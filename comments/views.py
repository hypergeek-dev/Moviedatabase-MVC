from django.shortcuts import render

# Function to add a comment to an article

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
            new_comment.news_article = article
            if request.user.is_authenticated:
                new_comment.name = request.user.username
                new_comment.email = request.user.email
            try:
                new_comment.save()
                # Handle successful comment save
                return JsonResponse({'result': 'Comment added successfully', 'comment_id': new_comment.id})
            except Exception as e:
                # Handle error during comment save
                return JsonResponse({'result': 'Failed to save comment'})
        else:
            # Handle invalid form
            return HttpResponseBadRequest('Invalid form')
    else:
        # Handle non-POST request (e.g., GET)
        form = CommentForm()
    
    return JsonResponse({'result': 'This was not a POST request'})

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
