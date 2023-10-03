from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from .models import Post
import requests
from django.conf import settings

# Function to fetch news from the API

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6

def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={settings.NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    admin_user = User.objects.get(username='admin_username')  
    for article in data['articles']:
        Post.objects.create(
            title=article['title'],
            slug=article['title'].replace(" ", "-"),
            author=admin_user,
            featured_image='placeholder',
            excerpt=article['description'][:100],
            content=article['description'],
            updated_on=article['publishedAt'],
            created_on=article['publishedAt'],
            status=1
        )
