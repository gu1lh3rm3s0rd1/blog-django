from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog.models import Post
from .forms import CommentForm
from django.contrib import messages


@login_required
def add_comment_to_post(request, pk):
    """
    View for adding a comment to a post. Requires user to be authenticated.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
        else:
            # Add an error message
            messages.error(request, 'There was an error with your submission. Please try again.')
    else:
        form = CommentForm()
    return render(request, 'comments/add_comment_to_post.html', {'form': form})
