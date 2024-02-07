from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    news_article = models.ForeignKey('qfb_main.NewsArticle', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', null=True)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    comment_content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.comment_content} by {self.name}"
