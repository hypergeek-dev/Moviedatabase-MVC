from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

STATUS = ((0, "Draft"), (1, "Published"))

class NewsArticle(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news_articles")
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    source_id = models.CharField(max_length=255)
    source_priority = models.IntegerField()
    country = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    pub_date = models.DateTimeField(null=True, blank=True)  
    image_url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    news_article = models.ForeignKey(NewsArticle, related_name='comments', on_delete=models.CASCADE)  # Changed from NewsArticle to news_article
    name = models.CharField(max_length=80)
    email = models.EmailField()
    comment_content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.comment_content} by {self.name}"
