from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
import requests
import json
import logging
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
import uuid
from qfb_main.models import NewsArticle
from .comments import CommentForm
import traceback
import spacy


# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to fetch news
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
                    doc = nlp(article.get('content', ''))
                    sentences = [sent.text for sent in doc.sents]
                    def group_into_paragraphs(sentences, n):
                        paragraphs = []
                        for i in range(0, len(sentences), n):
                            paragraph = " ".join(sentences[i:i+n])
                            paragraphs.append(paragraph)
                        return paragraphs
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
                            'pubDate': pub_date if pub_date_str else None,
                            'image_url': article.get('image_url', ''),
                            'status': 1
                        }
                    )
                    logging.debug(f"Saved article with ID: {article['article_id']}")
                except Exception as e:
                    tb_str = traceback.format_exception(type(e), e, e.__traceback__)
                    tb_str = "".join(tb_str)
                    logging.error(f"Failed to save article: {e}\n{tb_str}")
        except KeyError:
            logging.error(f"API response missing 'articles' key: {response.text}")
        except Exception as e:
            tb_str = traceback.format_exception(type(e), e, e.__traceback__)
            tb_str = "".join(tb_str)
            logging.error(f"An error occurred while processing the API response: {e}\n{tb_str}")
    else:
        logging.error(f"API call failed with status code {response.status_code}: {response.text}")

# Function to render news articles
def news_article_list(request):
    articles = NewsArticle.objects.filter(status=1)
    return render(request, 'index.html', {'NewsArticle_list': articles})

# Function to render individual news article details
def newsarticle_detail(request, id):
    article = get_object_or_404(NewsArticle, id=id)
    return render(request, 'newsarticle_detail.html', {'article': article})

def add_comment_to_article(request, article_id):
    article = get_object_or_404(NewsArticle, id=article_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form = CommentForm()

    return render(request, 'comments.html', {
        'article': article,
        'form': form,
    })

# Signup view
def account_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

# Login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

# Logout view
def user_logout(request):
    logout(request)
    return redirect('home')
