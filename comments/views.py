from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import CommentForm
from .models import Comment
from qfb_main.models import NewsArticle

@require_POST
def add_comment_to_article(request, article_id):
    """
    Adds a comment to an article identified by article_id.
    """
    article = get_object_or_404(NewsArticle, id=article_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.news_article = article
        if request.user.is_authenticated:
            new_comment.user = request.user
            new_comment.name = request.user.username
            new_comment.email = request.user.email
        new_comment.save()
        return JsonResponse({'success': True, 'message': 'Comment added successfully', 'comment_id': new_comment.id})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)

@require_POST
def edit_comment(request, comment_id):
    """
    Edits an existing comment identified by comment_id.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Comment edited successfully'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)

@require_POST
def delete_comment(request, comment_id):
    """
    Deletes an existing comment identified by comment_id.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return JsonResponse({'success': True, 'message': 'Comment deleted successfully'})
