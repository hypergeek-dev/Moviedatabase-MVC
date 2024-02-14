from django.test import TestCase, Client
from django.urls import reverse
from qfb_main.models import NewsArticle, User
from comments.models import Comment
from unittest.mock import patch
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAddCommentToArticle(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='testpassword')
        self.article = NewsArticle.objects.create(
            title='Test Article',
            slug='test-article',
            author=self.user,
            content='Test content',
            source_priority=1
        )
        self.form_data = {'comment_content': 'Test comment'}
        self.client.force_login(self.user)

    def test_valid_form_data(self):
        response = self.client.post(reverse('add_comment_to_article', kwargs={'article_id': self.article.id}), self.form_data)
        response_content = json.loads(response.content.decode('utf-8'))

        logger.info(f"Test valid form data: Status Code = {response.status_code}, Response = {response_content}")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_content['success'])
        self.assertEqual(response_content['message'], 'Comment added successfully')
        self.assertIsNotNone(response_content.get('comment_id', None))

    def test_authenticated_user(self):
        response = self.client.post(reverse('add_comment_to_article', kwargs={'article_id': self.article.id}), self.form_data)
        response_content = json.loads(response.content.decode('utf-8'))
        comment_id = response_content.get('comment_id')
        comment = Comment.objects.get(id=comment_id)

        logger.info(f"Test authenticated user can post comment: Comment User = {comment.user.username}, Expected User = {self.user.username}")

        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.name, self.user.username)
        self.assertEqual(comment.email, self.user.email)

    def test_invalid_http_method(self):
        response = self.client.get(reverse('add_comment_to_article', kwargs={'article_id': self.article.id}))

        logger.info(f"Test invalid HTTP method: Status Code = {response.status_code}, Expected = 405")

        self.assertEqual(response.status_code, 405)

    def test_article_not_found(self):
        response = self.client.post(reverse('add_comment_to_article', kwargs={'article_id': 99999}), self.form_data)

        logger.info(f"Test article not found: Status Code = {response.status_code}, Expected = 404")

        self.assertEqual(response.status_code, 404)

    def test_error_saving_comment(self):
        with patch('comments.views.Comment.save', side_effect=Exception('Error saving comment')):
            response = self.client.post(reverse('add_comment_to_article', kwargs={'article_id': self.article.id}), self.form_data)

            logger.info(f"Test error saving comment: Status Code = {response.status_code}, Expected = 500")

            self.assertEqual(response.status_code, 500)

    def test_associate_comment_with_article(self):
        response = self.client.post(reverse('add_comment_to_article', kwargs={'article_id': self.article.id}), self.form_data)
        response_content = json.loads(response.content.decode('utf-8'))
        comment_id = response_content.get('comment_id')
        comment = Comment.objects.get(id=comment_id)

        logger.info(f"Test associate comment with article: Comment Article ID = {comment.news_article.id}, Expected Article ID = {self.article.id}")

        self.assertEqual(comment.news_article, self.article)
