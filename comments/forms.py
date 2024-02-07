from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    comment_content = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment_content')
        