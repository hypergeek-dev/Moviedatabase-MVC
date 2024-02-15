from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_on')  
    list_filter = ('approved', 'created_on')  
    search_fields = ('name', 'email', 'comment_content') 

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Mark selected comments as approved"

admin.site.register(Comment, CommentAdmin)
