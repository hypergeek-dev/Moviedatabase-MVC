from django.core.management.base import BaseCommand
from qfb_main.views import fetch_news
import logging

# It's recommended to configure logging in settings.py for larger projects
logging.basicConfig(level=logging.DEBUG)

class Command(BaseCommand):
    """
    A custom Django management command to fetch news and store it in the database.
    """
    
    help = 'Fetches news from an external source and stores it in the database.'

    def handle(self, *args, **kwargs):
        """
        Executes the fetch_news function and handles success or failure.
        """
        try:
            fetch_news()
            self.stdout.write(self.style.SUCCESS('Successfully fetched news and stored it in the database.'))
            logging.debug("Successfully executed fetch_news")
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to fetch news and store it in the database.'))
            logging.error(f"Failed to execute fetch_news: {e}")
