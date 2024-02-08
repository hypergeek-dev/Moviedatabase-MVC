from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path("", views.news_article_list, name="home"),
    path('logout/', views.user_logout, name='logout'),
    path('feedback/', views.feedback_view, name='feedback'),
    path("article/<int:id>/", views.news_article_detail, name="newsarticle_detail"),
    path("account/login/", 
         auth_views.LoginView.as_view(template_name="account/login.html"), 
         name="account_login"),
    path("account/logout/", 
         auth_views.LogoutView.as_view(template_name="account/logout.html"), 
         name="account_logout"),
    path('account/signup/', views.account_signup, name='account_signup'),
    path('comments/', include('comments.urls')),
]
