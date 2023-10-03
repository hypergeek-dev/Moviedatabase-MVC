from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from .models import Post
import requests
from django.conf import settings

# Class-based view to list posts
class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6

# Function to fetch news from NewsData.io API and populate the Post model
def fetch_news():
    # Construct the URL for the NewsData.io API
    url = "https://newsdata.io/api/1/news?apikey=" + settings.NEWS_API_KEY
    
    # Make the API request
    response = requests.get(url)
    
    # Parse the JSON response
    data = response.json()
    print("API Response:", data)  # Debugging line

    # Check if the request was successful
    if data.get('Status') == 'success':
        # Get the admin user from the User model
        admin_user = User.objects.get(username=settings.DJANGO_ADMIN_USERNAME)

        # Loop through the articles in the API response
        for article in data.get('articles', []):  # Replace 'articles' with the correct key if different
            # Create a new Post object for each article
            Post.objects.create(
                title=article['title'],
                slug=article['title'].replace(" ", "-"),
                author=admin_user,
                featured_image=article['image_url'],  # Replace with 'image_url' or the correct key for images
                excerpt=article['description'][:100],
                content=article['content'],
                updated_on=article['pubDate'],
                created_on=article['pubDate'],
                status=1
            )
    else:
        print(f"Failed to fetch articles. Status: {data.get('Status')}, Message: {data.get('message', 'Unknown error')}")

