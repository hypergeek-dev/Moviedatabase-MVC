from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')  
    list_filter = ('created_at',)  
    search_fields = ('name', 'email', 'message') 

admin.site.register(Feedback, FeedbackAdmin)
