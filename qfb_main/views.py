from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from qfb_main.models import Post
import requests
from django.conf import settings
import logging  # Import the logging library

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

def fetch_news():
    url = "https://newsdata.io/api/1/news?apikey=" + settings.NEWS_API_KEY
    response = requests.get(url)
    data = response.json()
    logging.debug(f"API Response: {data}")  # Log the API response

    if data.get('Status') == 'success':
        admin_user = User.objects.get(username=settings.DJANGO_ADMIN_USERNAME)
        for article in data.get('articles', []):
            try:
                # Create a new Post object for each article
                Post.objects.create(
                    title=article['title'],
                    slug=article['title'].replace(" ", "-"),
                    author=admin_user,
                    featured_image=article['image_url'],
                    image_url=article['image_url'],
                    pubDate=article['pubDate'],
                    excerpt=article['description'][:100],
                    content=article['content'],
                    updated_on=article['pubDate'],
                    created_on=article['pubDate'],
                    status=1
                )
                logging.debug(f"Successfully saved article: {article['title']}")  # Log success
            except Exception as e:
                logging.error(f"Failed to save article: {e}")  # Log any exceptions
    else:
        logging.error(f"Failed to fetch articles. Status: {data.get('Status')}, Message: {data.get('message', 'Unknown error')}")
