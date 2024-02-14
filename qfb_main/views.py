import json
import logging
import os
import requests
import traceback
import uuid
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.utils.text import slugify

from comments.models import Comment
from feedback.forms import FeedbackForm
from qfb_main.models import NewsArticle

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
        request: HttpRequest object, optional.

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
                    doc = nlp(article.get('content', ''))
                    sentences = [sent.text for sent in doc.sents]

                    paragraphs = group_into_paragraphs(sentences, 5)
                    formatted_content = "\n\n".join(paragraphs)
                    news_article, created = NewsArticle.objects.update_or_create(
                        title=article['title'],
                        defaults={
                            'slug': slug,
                            'content': formatted_content,
                            'author_id': 1,
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
    Fetches a list of news articles from the database, paginates them, and renders 
    the list to the 'index.html' template.

    This function filters the articles by their status (only articles with a status of 1 are included),
    orders them by their publication date in descending order, and paginates the results with a fixed
    number of articles per page (currently set to 3).

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse object with the rendered 'index.html' template including the paginated list of news articles,
        a flag indicating whether pagination is necessary ('is_paginated'), and the paginator's 'page_obj' for the current page.
    """
    articles_list = NewsArticle.objects.filter(Q(status=1)).order_by('-pub_date')
    paginator = Paginator(articles_list, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'news_article_list': page_obj,  
        'is_paginated': True if paginator.num_pages > 1 else False, 
        'page_obj': page_obj 
    })

    
def news_article_detail(request, id):
    article = get_object_or_404(NewsArticle, id=id)
    return render(request, 'news_article_detail.html', {'article': article})


def feedback_view(request):
    """
    Handles the feedback form submission. If the request is POST and the form is valid,
    it saves the feedback and redirects to the 'home' page with a success message. If the
    form is invalid, it displays error messages. For GET requests, it displays a blank feedback form.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse object with the rendered 'feedback.html' template including the form instance.
    """
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
    """
    Handles user registration via the UserCreationForm. If the request is POST and the form is valid,
    it creates a new user, logs them in, and redirects to the 'home' page with a success message. If the
    form is invalid, it displays error messages. For GET requests, it displays a blank registration form.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse object with the rendered 'account/signup.html' template including the form instance.
    """

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
    """
    Handles user login via the AuthenticationForm. If the request is POST and the form is valid,
    it logs the user in and redirects to the 'home' page with a success message. If the form is
    invalid, it displays error messages. For GET requests, it displays the login form.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse object with the rendered 'account/login.html' template including the form instance.
    """

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
    """
    Logs out the user and redirects to the 'home' page with an informational message about the logout.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponseRedirect object to redirect the user to the 'home' page after logout.
    """

    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

