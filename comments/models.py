from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    """
    Model representing a comment made on a news article.
    """
    news_article = models.ForeignKey('qfb_main.NewsArticle', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', null=True)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    content = models.TextField()  # Renamed for simplicity
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.content} by {self.name}"
