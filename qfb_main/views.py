import os
import requests
import json
import logging
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify 
import uuid 
from qfb_main.models import NewsArticle

def fetch_news():
    api_key = os.getenv('NEWS_API_KEY')
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&country=us&language=en"
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            data = json.loads(response.text)
            articles = data['results']

            for article in articles:
                try:
                    pub_date_str = article.get('pubDate', None)
                    if pub_date_str:
                        pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d %H:%M:%S')  
                        pub_date = timezone.make_aware(pub_date)

              
                    slug = slugify(article['title']) + '-' + str(uuid.uuid4())[:8]

                    news_article, created = NewsArticle.objects.update_or_create(
                        article_id=article['article_id'],
                        defaults={
                            'title': article['title'],
                            'slug': slug,  
                            'content': article.get('description', ''), 
                            'author_id': 1,  
                            'source_id': article['source_id'],
                            'source_priority': article['source_priority'],
                            'category': ','.join(article['category']), 
                            'language': article['language'],
                            'pubDate': pub_date if pub_date_str else None,
                            'image_url': article.get('image_url', ''), 
                        }
                    )
                    logging.debug(f"Saved article with ID: {article['article_id']}")
                except Exception as e:
                    logging.error(f"Failed to save article: {e}")
        except KeyError:
            logging.error(f"API response missing 'articles' key: {response.text}")
        except Exception as e:
            logging.error(f"An error occurred while processing the API response: {e}")
    else:
        logging.error(f"API call failed with status code {response.status_code}: {response.text}")
