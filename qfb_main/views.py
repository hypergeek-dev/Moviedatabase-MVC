from dotenv import load_dotenv
import os
load_dotenv()
import requests
import json
from qfb_main.models import NewsArticle 
import logging



def fetch_news():
    api_key = os.getenv('NEWS_API_KEY')
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&country=us&language=en&limit=10"
    response = requests.get(url)
    data = json.loads(response.text)
    articles = data['articles']
    
    for article in articles:
        try:
            news_article, created = NewsArticle.objects.update_or_create(
                article_id=article['article_id'],
                defaults={
                    'title': article['title'],
                    'content': article['content'],
                    'excerpt': article['description'],
                    'source_id': article['source_id'],
                    'source_priority': article['source_priority'],
                    'country': article['country'],
                    'category': article['category'],
                    'language': article['language'],
                    'pubDate': article['pubDate'],
                }
            )
            logging.debug(f"Saved article with ID: {article['article_id']}")
        except Exception as e:
            logging.error(f"Failed to save article: {e}")
