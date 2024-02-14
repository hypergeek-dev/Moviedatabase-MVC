from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from feedback.forms import FeedbackForm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedbackViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123password')
        self.client.login(username='testuser', password='123password')

    def test_feedback_view_get_request(self):
        """
        Test that the feedback view returns the correct template and form with a GET request.
        """
        response = self.client.get(reverse('feedback'))

        logger.info(f"Test feedback view GET request: Status Code = {response.status_code}, Template Used = 'feedback.html'")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback.html')
        self.assertIsInstance(response.context['form'], FeedbackForm)

    def test_feedback_view_post_request_invalid(self):
        invalid_data = {
            'name': '',
            'email': 'user@test.com',
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('feedback'), invalid_data)

        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        logger.info(f"Test feedback view POST request with invalid data: Status Code = {response.status_code}, Form Errors = {response.context['form'].errors}, Messages = {messages}")

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')
