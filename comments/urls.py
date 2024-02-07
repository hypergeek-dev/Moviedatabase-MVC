from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views  
    
    
path("comment_display/<int:article_id>/", views.add_comment_to_article, name="comment_display"),
path("comment_form/<int:id>/", views.edit_comment, name="comment_form"),