from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import CommentForm
from .models import Comment
from qfb_main.models import NewsArticle
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_protect

@require_POST
@csrf_protect 
@login_required  
def add_comment_to_article(request, article_id):
    """
    Adds a comment to an article identified by article_id.
    """
    article = get_object_or_404(NewsArticle, id=article_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.news_article = article

        new_comment.user = request.user
        new_comment.name = request.user.username
        new_comment.email = request.user.email
        try:
            new_comment.save()
            return JsonResponse({'success': True, 'message': 'Comment added successfully', 'comment_id': new_comment.id})
        except Exception as e:  
            return JsonResponse({'success': False, 'error': 'Failed to save comment'}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)

@require_POST
@login_required
def edit_comment(request, comment_id):
    """
    Edits an existing comment identified by comment_id.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if not request.user == comment.user:
        raise PermissionDenied("You do not have permission to edit this comment.")
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({'success': True, 'message': 'Comment edited successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Failed to edit comment'}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)
    
@require_POST
@login_required
def delete_comment(request, comment_id):
    """
    Deletes an existing comment identified by comment_id.
    """
    comment = get_object_or_404(Comment, id=comment_id)

    if not request.user == comment.user:
        raise PermissionDenied("You do not have permission to delete this comment.")
    try:
        comment.delete()
        return JsonResponse({'success': True, 'message': 'Comment deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Failed to delete comment'}, status=500)