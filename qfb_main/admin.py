from django.contrib import admin
from .models import NewsArticle
from django_summernote.admin import SummernoteModelAdmin

@admin.register(NewsArticle)
class NewsArticleAdmin(SummernoteModelAdmin):
    """
    Admin view for editing NewsArticle models with enhanced features
    provided by SummernoteModelAdmin for rich text editing.
    """
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

    def has_change_permission(self, request, obj=None):
        """
        Ensure that only superusers can change news article entries.
        
        Args:
            request: HttpRequest object.
            obj: The object being changed; None if this is a 'change list' page.
            
        Returns:
            bool: True if the user is a superuser, False otherwise.
        """
        return request.user.is_superuser
