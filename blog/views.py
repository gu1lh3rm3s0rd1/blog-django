# from .models import Comment
from django.shortcuts import get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages

from comments.models import Comment
from comments.forms import CommentForm
from .models import Post
from .forms import PostForm
from comments.models import Reply
from comments.forms import ReplyForm


def home(request):
    posts_list = Post.objects.all().order_by('created_at')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'blog/home.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    content_type = ContentType.objects.get_for_model(Post)

    if request.method == "POST":
        comment_form = CommentForm(request.POST, initial={
            'content_type': content_type,
            'object_id': post.id
        })

        if comment_form.is_valid():
            obj_id = comment_form.cleaned_data.get('object_id')
            content_data = comment_form.cleaned_data.get('content')
            new_comment = Comment.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=obj_id,
                content=content_data,
                post=post
            )
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm(initial={
            'content_type': content_type,
            'object_id': post.id
        })

    posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form, 'posts': posts})


@login_required
def create_post(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Sem permissão para criar posts.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if not request.user.is_superuser:
        return HttpResponseForbidden("Sem permissão para editar posts.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def about(request):
    return render(request, 'blog/about.html')


@login_required
def reply_to_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.user = request.user
            reply.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = ReplyForm()
    return render(request, 'blog/post_detail.html', {'form': form})


@login_required
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        messages.error(request, "Sem comentários.")
        return redirect('home')

    if request.user == comment.user or request.user.is_staff:
        comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def delete_reply(request, pk):
    try:
        reply = Reply.objects.get(pk=pk)
    except Reply.DoesNotExist:
        return HttpResponseNotFound("Sem respostas.")
    if request.user == reply.user or request.user.is_staff:
        post_pk = reply.comment.post.pk
        reply.delete()
    return redirect('post_detail', pk=post_pk)
