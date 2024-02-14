from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from qfb_main.models import NewsArticle
from django.contrib.auth.models import User
from django.utils import timezone
from qfb_main.views import group_into_paragraphs, make_api_call
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestMakeApiCall(TestCase):

    @patch('qfb_main.views.requests.get')
    def test_make_api_call_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'key': 'value'}

        response = make_api_call()

        logger.info(f"Test make_api_call success: Status Code = {response.status_code}, Response = {response.json()}")

        self.assertEqual(response.status_code, 200)

class TestGroupIntoParagraphs(TestCase):

    def test_group_into_paragraphs(self):
        sentences = ['Sentence 1.', 'Sentence 2.', 'Sentence 3.', 'Sentence 4.', 'Sentence 5.', 'Sentence 6.']
        expected_paragraphs = ['Sentence 1. Sentence 2. Sentence 3. Sentence 4. Sentence 5.', 'Sentence 6.']

        paragraphs = group_into_paragraphs(sentences, 5)

        logger.info(f"Test group_into_paragraphs: Expected Paragraphs = {expected_paragraphs}, Result = {paragraphs}")

        self.assertEqual(paragraphs, expected_paragraphs)

class TestNewsArticleViews(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345')

        # Directly set status to 1 here
        self.article = NewsArticle.objects.create(
            title="Test Article",
            slug="test-article",
            author=self.test_user,
            excerpt="Test excerpt",
            content="Test content",
            status=1,  # Correctly set status here
            source_id="source_123",
            source_priority=1,
            country="Test Country",
            category="Test Category",
            language="en",
            pub_date=timezone.now(),
            image_url="http://example.com/test.jpg",
        )

    def test_news_article_list_view(self):
        response = self.client.get(reverse('home'))

        logger.info(f"Test news_article_list_view: Status Code = {response.status_code}, Contains 'Test Article' = {'Test Article' in response.content.decode()}")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Article")

