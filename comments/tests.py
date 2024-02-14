from django.test import TestCase, Client
from django.urls import reverse
from qfb_main.models import NewsArticle, User
from comments.models import Comment
from unittest.mock import patch
import json

class TestAddCommentToArticle(TestCase):
    def setUp(self):
        # Setup code remains largely the same, using Client for authenticated requests
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='testpassword')
        self.article = NewsArticle.objects.create(
            title='Test Article', 
            slug='test-article', 
            author=self.user, 
            content='Test content', 
            source_priority=1  # Ensure to provide this value as it is required
        )
        self.form_data = {'comment_content': 'Test comment'}
        self.client.force_login(self.user)

    def test_valid_form_data(self):
        # Adjusted to use the client.post method for sending requests
        response = self.client.post(reverse('add_comment_to_article', kwargs={'article_id': self.article.id}), self.form_data)
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_content['success'])
        self.assertEqual(response_content['message'], 'Comment added successfully')
        self.assertIsNotNone(response_content.get('comment_id', None))

    def test_authenticated_user(self):
        # This test verifies if a comment can be associated with an authenticated user
        response = self.client.post(reverse('add_comment_to_article', kwargs={'article_id': self.article.id}), self.form_data)
        response_content = json.loads(response.content.decode('utf-8'))
        comment_id = response_content.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.name, self.user.username)
        self.assertEqual(comment.email, self.user.email)

    def test_invalid_http_method(self):
        # Test adjusted for HttpResponseNotAllowed
        response = self.client.get(reverse('add_comment_to_article', kwargs={'article_id': self.article.id}))
        self.assertEqual(response.status_code, 405)  # HTTP 405 Method Not Allowed

    def test_article_not_found(self):
        # Adjusted for article not found scenario
        response = self.client.post(reverse('add_comment_to_article', kwargs={'article_id': 99999}), self.form_data)
        self.assertEqual(response.status_code, 404)

    def test_error_saving_comment(self):
        # Assuming 'add_comment_to_article' is in the 'comments' app and 'views.py' file
        with patch('comments.views.Comment.save', side_effect=Exception('Error saving comment')):
            response = self.client.post(reverse('add_comment_to_article', kwargs={'article_id': self.article.id}), self.form_data)
            self.assertEqual(response.status_code, 500)

    def test_associate_comment_with_article(self):
        # Verify comment is associated with the correct article
        response = self.client.post(reverse('add_comment_to_article', kwargs={'article_id': self.article.id}), self.form_data)
        response_content = json.loads(response.content.decode('utf-8'))
        comment_id = response_content.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        self.assertEqual(comment.news_article, self.article)
