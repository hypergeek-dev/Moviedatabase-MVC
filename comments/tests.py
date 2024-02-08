# Assuming the following imports are correctly set up in your tests.py or a similar test module
from django.test import TestCase, RequestFactory
from django.urls import reverse
from qfb_main.models import NewsArticle, User
from comments.models import Comment 
from comments.views import add_comment_to_article
from unittest.mock import patch
from django.http import HttpResponse

class TestAddCommentToArticle(TestCase):
    def setUp(self):
        # Common setup for all tests
        self.factory = RequestFactory()
        self.user = User.objects.create(username='test_user', email='test@example.com')
        self.article = NewsArticle.objects.create(title='Test Article', slug='test-article', author=self.user, content='Test content')
        self.form_data = {'comment_content': 'Test comment'}

    def test_valid_form_data(self):
        request = self.factory.post('/add_comment/{}'.format(self.article.id), self.form_data)
        request.user = self.user

        response = add_comment_to_article(request, self.article.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], 'Comment added successfully')
        self.assertIsNotNone(response.json()['comment_id'])

    def test_authenticated_user(self):
        request = self.factory.post('/add_comment/{}'.format(self.article.id), self.form_data)
        request.user = self.user

        response = add_comment_to_article(request, self.article.id)

        comment = Comment.objects.get(id=response.json()['comment_id'])
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.name, self.user.username)
        self.assertEqual(comment.email, self.user.email)

    def test_invalid_http_method(self):
        request = self.factory.get('/add_comment/{}'.format(self.article.id))

        response = add_comment_to_article(request, self.article.id)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['error'], 'HTTP method not allowed')

    def test_article_not_found(self):
        # Assuming a very high ID that won't exist
        request = self.factory.post('/add_comment/99999', self.form_data)

        response = add_comment_to_article(request, 99999)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Article not found')

    def test_error_saving_comment(self):
        request = self.factory.post('/add_comment/{}'.format(self.article.id), self.form_data)

        with patch('myapp.models.Comment.save', side_effect=Exception('Error saving comment')):
            response = add_comment_to_article(request, self.article.id)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['error'], 'Failed to save comment')

    def test_associate_comment_with_article(self):
        request = self.factory.post('/add_comment/{}'.format(self.article.id), self.form_data)

        response = add_comment_to_article(request, self.article.id)

        comment = Comment.objects.get(id=response.json()['comment_id'])
        self.assertEqual(comment.news_article, self.article)
