from django.core.management.base import BaseCommand
from qfb_main.views import fetch_news
import logging  # Import the logging library

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

class Command(BaseCommand):
    help = 'Calls the fetch_news function to fetch news from the API and store it in the database.'

    def handle(self, *args, **kwargs):
        try:
            fetch_news()
            self.stdout.write(self.style.SUCCESS('Successfully fetched news and stored it in the database'))
            logging.debug("Successfully executed fetch_news")  # Log success
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to fetch news and store it in the database'))
            logging.error(f"Failed to execute fetch_news: {e}")  # Log any exceptions
