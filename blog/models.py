from django.db import models
from django.utils import timezone
from accounts.models import Profile


class Post(models.Model):
    user            = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title           = models.CharField(max_length=50)
    img             = models.ImageField(upload_to='img/posts', blank=True, null=True)
    content         = models.TextField()
    created_at      = models.DateTimeField(default=timezone.now)
    updated_at      = models.DateTimeField(auto_now=True)
    is_published    = models.BooleanField(default=True) 
     
    def __str__(self):
        return self.title
    
    def short_content(self):
        return self.content[:100]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    def __str__(self):
        return f'{self.user.username} - {self.text}'