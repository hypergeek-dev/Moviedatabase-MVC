from django.shortcuts import render
from django.views import generic
from qfb_main.models import NewsArticle

class NewsArticleList(generic.ListView):
    model = NewsArticle
    queryset = NewsArticle.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6