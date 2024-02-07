from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from .forms import CommentForm
from qfb_main.models import NewsArticle

def add_comment_to_article(request, article_id):
    try:
        article = get_object_or_404(NewsArticle, id=article_id)
    except Exception as e:
        # Handle article not found error
        return JsonResponse({'result': 'Article not found'})

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.news_article = article  # Assuming your Comment model has a field to link it to NewsArticle
            if request.user.is_authenticated:
                new_comment.user = request.user  # Associate the comment with the currently logged-in user
                new_comment.name = request.user.username  # Assuming you still want to use these fields
                new_comment.email = request.user.email
            try:
                new_comment.save()
                return JsonResponse({'result': 'Comment added successfully', 'comment_id': new_comment.id})
            except Exception as e:
                return JsonResponse({'result': 'Failed to save comment'})
        else:
            return HttpResponseBadRequest('Invalid form')
    else:
        form = CommentForm()
        return render(request, 'index.html', {'form': form, 'article_id': article_id})


# Function to edit a comment
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            edited_comment = form.save()
            return JsonResponse({'result': 'Comment edited successfully'})
        else:
            return HttpResponseBadRequest('Invalid form')
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})
# Function to delete a comment
def delete_comment(request, article_id, comment_id):

    try:
        comment = Comment.objects.get(id=comment_id, article__id=article_id)
        comment.delete()
        return JsonResponse({'result': 'Comment deleted successfully'})
    except Comment.DoesNotExist:
        return JsonResponse({'result': 'Comment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'result': f'Error: {str(e)}'}, status=500)
