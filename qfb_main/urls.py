from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path("", views.news_article_list, name="home"),  
    path("article/<int:id>/", views.newsarticle_detail, name="newsarticle_detail"),
]
