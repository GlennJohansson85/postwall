from django.db import models
from django.utils import timezone
from accounts.models import Profile


class Post(models.Model):
    """
    A model representing a blog post.

    Is used to store information about individual posts created by users.
    It includes fields for the post's title, content, associated user, and DateTime as metadata.
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to='img/posts', blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def short_content(self):
        return self.content[:100]


class Comment(models.Model):
    """
    A model representing a comment on a blog post.

    Is used to store user comments associated with a specific post.
    It includes fields for the comment text, the user who made the comment,
    and the post it relates to.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.text}'
