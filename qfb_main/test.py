from qfb_main.views import group_into_paragraphs
from unittest.mock import patch
from django.test import TestCase
from qfb_main.views import make_api_call
from django.urls import reverse
from qfb_main.models import NewsArticle
from django.contrib.auth.models import User
from django.utils import timezone
from qfb_main.models import NewsArticle

class TestMakeApiCall(TestCase):

    @patch('qfb_main.views.requests.get')
    def test_make_api_call_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'key': 'value'}

        response = make_api_call()
        self.assertEqual(response.status_code, 200)

class TestGroupIntoParagraphs(TestCase):

    def test_group_into_paragraphs(self):
        sentences = ['Sentence 1.', 'Sentence 2.', 'Sentence 3.', 'Sentence 4.', 'Sentence 5.', 'Sentence 6.']
        expected_paragraphs = ['Sentence 1. Sentence 2. Sentence 3. Sentence 4. Sentence 5.', 'Sentence 6.']
        
        paragraphs = group_into_paragraphs(sentences, 5)
        self.assertEqual(paragraphs, expected_paragraphs)

class TestNewsArticleViews(TestCase):

    def setUp(self):

        test_user = User.objects.create_user(username='testuser', password='12345')

        valid_status = 0


        NewsArticle.objects.create(
            title="Test Article",
            slug="test-article",
            author=test_user,
            excerpt="Test excerpt",
            content="Test content",
            status=valid_status,
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
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Test Article")