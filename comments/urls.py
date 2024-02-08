from django.urls import path
from . import views

# URL patterns for comment-related actions
urlpatterns = [
    path('add_comment/<int:article_id>/', views.add_comment_to_article, name='add_comment_to_article'),
    path("edit_comment/<int:comment_id>/", views.edit_comment, name="edit_comment"),
    path("delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),
]
