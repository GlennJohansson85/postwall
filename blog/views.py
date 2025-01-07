from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages

from .forms import PostForm, CommentForm
from .models import Post, Comment


def postwall(request):
    """
    Renders the postwall page displaying all published posts along with their comments.

    Retrieves all posts and their associated comments.
    The posts are sorted in descending order based on their date, allowing users to see the
    most recent posts first. The context also includes the current logged-in user, enabling user-specific
    functionalities, such as adding comments.
    """
    # Retrieve all published posts, sorted in descending order by their creation date.
    posts_with_comments = []
    # Initialize a list to hold posts and their associated comments.
    posts = Post.objects.filter(is_published=True).order_by('-created_at')

    # Iterate through each post to fetch its comments.
    for post in posts:
        # Get all comments related to the current post
        comments = post.comments.all()
        # Append a dictionary containing the post and its comments to the list.
        posts_with_comments.append({'post': post, 'comments': comments})

    # Prepare the context data to be passed to the template.
    context = {
        # List of posts and comments for rendering
        'posts_with_comments': posts_with_comments,
        # The currently logged-in user
        'user': request.user,
    }

    # Render the 'postwall.html' template with the context data.
    return render(request, "postwall.html", context)


@login_required
def post(request):
    """
    Allows signed-in users to create a new post.

    Displays a form for creating a new post. When the form is submitted via a POST request,
    it validates the input data and, if valid, saves the post with the current user as the author.
    After successfully saving the post, the user is redirected to the postwall page.
    If the request method is GET, an empty form is presented to the user for input.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('postwall')

    else:
        form = PostForm()

    context = {
        'form': form
    }
    return render(request, 'post.html', context)


def post_detail(request, post_id):
    """
    Renders the details of a specific post.

    Retrieves a post identified by its `post_id` and displays it along with all comments
    associated with the post. Users can see the larger version of the post's image and all comments
    related to that post. The post uploader/admin can delete the post/comments.
    """
    # Get the post by ID or return a 404 error if not found
    post = get_object_or_404(Post, id=post_id)
    # Fetch all related comments for that post
    comments = post.comments.all()

    # Check if the request is a POST (indicating a form submission)
    if request.method == 'POST':
        # Instantiate a CommentForm with the submitted data.
        comment_form = CommentForm(request.POST)

        # If CommentForm is valid
        if comment_form.is_valid():
            # Get the profile of the currently logged-in user
            profile = get_object_or_404(Profile, user=request.user)
            # Save the comment form with the associated profile and post
            comment_form.save(user=profile, post=post)
            # Redirect the user to the postwall page after successfully saving the comment
            return redirect('postwall')

    # If not POST, create an empty CommentForm instance for displaying the form
    else:
        comment_form = CommentForm()

    # Prepare the data (post, comments, form, current user) to pass to the template
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user': request.user,
    }

    # Render the 'post_detail.html' template with the context data.
    return render(request, 'post_detail.html', context)


@login_required
def add_comment(request, post_id):
    """
    Allows signed-in users to submit comments to the posts.

    Signed-in users can submit comments directly from the postwall without needing
    to go to the post details. A success message is displayed when a comment is
    successfully submitted, and the user is redirected back to post where the comment
    was made (scroll_to_post.js) in postwall.html.
    Only signed in users can add comments.
    """
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')

        if comment_text:
            Comment.objects.create(
                post = post,
                user = request.user,
                text = comment_text
            )
            messages.success(request, 'Comment added successfully!')
            return redirect(f"{reverse('postwall')}?post_id={post.id}")
        else:
            messages.error(request, 'Comment cannot be empty.')
    return redirect('postwall')


@login_required
def delete_post_confirmation(request, post_id):
    """
    Handles the confirmation and deletion of a post.

    Retrieves a post by its `post_id` and displays a confirmation pop up to the user.
    If the user confirms the deletion (via a POST request), the post is deleted,
    and the user is redirected to the 'postwall' page. Only signed-in users/admin
    can delete posts.
    """
    # Retrieve the post by its ID, or return a 404 error if not found
    post = get_object_or_404(Post, id=post_id)

    # Check if the request method is POST (indicating the user has confirmed the deletion)
    if request.method == "POST":
        # Delete the post from the database
        post.delete()
        # Redirect the user to the 'postwall' page after deletion
        return redirect('postwall')

    # If the request method is not POST (i.e., GET), render the confirmation pop up
    context = {'post': post}
    return render(request, 'delete_post_confirmation.html', context)


@login_required
def delete_post(request, post_id):
    """
    Handles the deletion of a post.

    Retrieves a post by its `post_id` and checks if the current user is either the post's author
    or an admin. If the user is authorized, the post is deleted after confirmation, and a success message is displayed.
    Unauthorized users receive a forbidden response.
    """
    # Retrieve the post by its ID, or return a 404 error if not found
    post = get_object_or_404(Post, id=post_id)

    # Check if the logged-in user is the post's author or an admin
    if request.user == post.user or request.user.is_admin:
        # Delete the post from the database
        post.delete()
        # Display a success message to the user
        messages.success(request, 'The post has been successfully deleted.')
        # Redirect the user to the 'postwall' page after deletion
        return redirect('postwall')
    else:
        # Return a forbidden response if the user is not authorized
        return HttpResponseForbidden("You are not authorized to delete this post.")


@login_required
def delete_comment(request, comment_id):
    """
    Handles the deletion of a comment.

    Retrieves a comment by its `comment_id` and checks if the current user is either the comment's author
    or an admin. If the user is authorized, the comment is deleted, and a success message is displayed.
    Unauthorized users receive a forbidden response.
    """
    # Retrieve the comment by its ID, or return a 404 error if not found
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the logged-in user is the comment's author or an admin
    if request.user == comment.user or request.user.is_admin:
        # Delete the comment from the database
        comment.delete()
        # Display a success message to the user
        messages.success(request, 'The comment has been successfully deleted.')
        # Redirect the user to the post detail page that the comment belongs to
        return redirect('post_detail', post_id=comment.post.id)

    else:
        # Return a forbidden response if the user is not authorized
        return HttpResponseForbidden("You are not authorized to delete this comment.")


def search(request):
    """
    Handles the search functionality for posts.

    This view retrieves posts from the database that match the given keyword
    in their titles. If a keyword is provided in the GET request, it filters
    the posts accordingly. The results are then rendered in the
    'search_results.html' template.
    """
    # Retrieve the search keyword from the GET parameters, defaulting to an empty string if not provided
    keyword = request.GET.get('keyword', '')
    # Initialize an empty list to hold the matching posts
    posts = []

    # If a keyword is provided, filter posts that contain the keyword in their titles
    if keyword:
        posts = Post.objects.filter(title__icontains=keyword)

    # Render the 'search_results.html' template with the list of matching posts
    return render(request, 'search_results.html', {'posts': posts})


def search_suggestions(request):
    """
    Provides search suggestions based on the keyword.

    This view responds to AJAX requests by returning a JSON object containing
    suggested post titles that match the given keyword. The suggestions are
    limited to a maximum of 10 results.
    """
    # Retrieve the search keyword from the GET parameters, defaulting to an empty string if not provided
    keyword = request.GET.get('keyword', '')

    # Initialize an empty list to hold the suggested Post titles
    suggestions = []

    # If a keyword is provided, filter posts that contain the keyword in their titles
    if keyword:
        # Limit results to 10
        posts = Post.objects.filter(title__icontains=keyword)[:10]
        # Create a list of dictionaries with post id and title for each matching post
        suggestions = [{'id': post.id, 'title': post.title} for post in posts]

    # Return the suggestions as a JSON response
    return JsonResponse({'suggestions': suggestions})
