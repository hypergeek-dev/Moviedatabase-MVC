from django.contrib import admin
from .models import NewsArticle
from django_summernote.admin import SummernoteModelAdmin

@admin.register(NewsArticle)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

