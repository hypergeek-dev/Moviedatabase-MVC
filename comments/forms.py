from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    comment_content = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Comment
        fields = ('comment_content',)
