from django import forms
from .models import Comment
from .models import Feedback

class CommentForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    comment_content = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment_content')
        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']