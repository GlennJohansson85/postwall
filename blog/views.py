from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import PostForm, CommentForm
from .models import Post, Comment


def postwall(request):
    posts_with_comments = []
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    for post in posts:
        comments = post.comments.all()
        posts_with_comments.append({'post': post, 'comments': comments})
    
    context = {
        'posts_with_comments': posts_with_comments,
        'user': request.user, 
    }
    return render(request, "postwall.html", context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(
                post=post,
                user=request.user,
                text=comment_text
            )
    return redirect('postwall')


@login_required
def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('postwall')
    else:
        form    = PostForm()
    context     = {
        'form': form
    }
    
    return render(request, 'post.html', context)   


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            profile = request.user
            comment_form.save(user=profile, post=post)
            return redirect('postwall')
    
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user': request.user,
    }
    return render(request, 'post_detail.html', context)


@login_required
def delete_post_confirmation(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        post.delete()
        return redirect('postwall')
    
    context = {'post': post}
    return render(request, 'delete_post_confirmation.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user == post.user or request.user.is_admin:
        post.delete()
        messages.success(request, 'The post has been successfully deleted.')
        return redirect('postwall')
    else:
        return HttpResponseForbidden("You are not authorized to delete this post.")


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user == comment.user or request.user.is_admin:
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)
    
    else:
        return HttpResponseForbidden("You are not authorized to delete this comment.")