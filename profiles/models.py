from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
    # stalker will give me who I'm following
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    # prey will give me who is following me
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)

class Post(models.Model):
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
