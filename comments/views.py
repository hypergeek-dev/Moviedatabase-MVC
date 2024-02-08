from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .forms import CommentForm
from .models import Comment
from qfb_main.models import NewsArticle
def add_comment_to_article(request, article_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'HTTP method not allowed'}, status=405)

    try:
        article = get_object_or_404(NewsArticle, id=article_id)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Article not found'}, status=404)

    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.news_article = article
        if request.user.is_authenticated:
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

def edit_comment(request, comment_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'HTTP method not allowed'}, status=405)

    comment = get_object_or_404(Comment, id=comment_id)
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({'success': True, 'message': 'Comment edited successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Failed to edit comment'}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)


def delete_comment(request, comment_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'HTTP method not allowed'}, status=405)

    try:
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return JsonResponse({'success': True, 'message': 'Comment deleted successfully'})
    except Comment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Comment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error: {str(e)}'}, status=500)

