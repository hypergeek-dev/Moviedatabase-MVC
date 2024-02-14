import json
import logging
import os
import traceback
import uuid
from datetime import datetime

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify

from comments.forms import CommentForm
from comments.models import Comment
from feedback.forms import FeedbackForm
from qfb_main.models import NewsArticle
import spacy
from spacy.lang.en import English

logger = logging.getLogger(__name__)


def make_api_call():
    """
    Makes an API call to fetch news data.
    
    Returns:
        Response object from the news API call.
    """
    api_key = os.getenv('NEWS_API_KEY')
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&country=us&language=en"
    return requests.get(url)


def fetch_news(request=None):
    """
    Fetches news from an API and processes the data.
    
    Args:
        request: HttpRequest object.
        
    Processes the fetched news data and stores it in the database.
    """
    response = make_api_call()
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
                    # Assuming 'nlp' object is predefined and accessible
                    doc = nlp(article.get('content', ''))
                    sentences = [sent.text for sent in doc.sents]

                    paragraphs = group_into_paragraphs(sentences, 5)
                    formatted_content = "\n\n".join(paragraphs)
                    news_article, created = NewsArticle.objects.update_or_create(
                        title=article['title'],
                        defaults={
                            'slug': slug,
                            'content': formatted_content,
                            'author_id': 1,  # Assuming a default author ID
                            'source_id': article['source_id'],
                            'source_priority': article['source_priority'],
                            'category': ','.join(article['category']),
                            'language': article['language'],
                            'pub_date': pub_date if pub_date_str else None,
                            'image_url': article.get('image_url', ''),
                            'status': 1
                        }
                    )
                    if request:
                        messages.success(request, f"Article saved with ID: {news_article.id}")
                except Exception as e:
                    tb_str = traceback.format_exception(type(e), e, e.__traceback__)
                    logger.error(f"Failed to save article: {e}\n{''.join(tb_str)}")
        except KeyError:
            logger.error(f"API response missing 'results' key: {response.text}")
        except Exception as e:
            tb_str = traceback.format_exception(type(e), e, e.__traceback__)
            logger.error(f"An error occurred while processing the API response: {e}\n{''.join(tb_str)}")
    else:
        logger.error(f"API call failed with status code {response.status_code}: {response.text}")


def group_into_paragraphs(sentences, n=5):
    """
    Groups sentences into paragraphs.
    
    Args:
        sentences: A list of sentences to group.
        n: Number of sentences per paragraph.
        
    Returns:
        A list of paragraphs.
    """
    paragraphs = []
    for i in range(0, len(sentences), n):
        paragraph = " ".join(sentences[i:i+n])
        paragraphs.append(paragraph)
    return paragraphs

def news_article_list(request):
    """
    Renders a list of news articles.
    
    Args:
        request: HttpRequest object.
        
    Returns:
        HttpResponse object with the rendered news article list template.
    """
    articles = NewsArticle.objects.filter(Q(status=1))
    return render(request, 'index.html', {'news_article_list': articles})


def news_article_detail(request, id):
    article = get_object_or_404(NewsArticle, id=id)
    return render(request, 'news_article_detail.html', {'article': article})


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your feedback has been submitted successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})



def account_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have signed up successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'account/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

