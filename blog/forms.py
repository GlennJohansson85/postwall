from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    For creating and updating Post instances.

    Allows users to input a title, image and content for their posts.
    Linked to the Post model.
    """
    class Meta:
        model = Post
        fields = ['title', 'img', 'content',]


class CommentForm(forms.ModelForm):
    """
    For creating and updating Comment instances.

    Allows users to submit comments to uploaded posts.
    """
    class Meta:
        model = Comment
        fields = ['text']

    def save(self, user, post, commit=True):
        comment = super().save(commit=False)
        comment.user = user
        comment.post = post

        if commit:
            comment.save()
        return comment
