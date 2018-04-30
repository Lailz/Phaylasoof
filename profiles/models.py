from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
    # stalker will give me who I'm following
    stalker = models.ForeignKey(User, related_name="stalker", on_delete=models.CASCADE)
    # prey will give me who is following me
    prey = models.ForeignKey(User, related_name="prey", on_delete=models.CASCADE)

class Clue(models.Model):
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clue = models.ForeignKey(Clue, on_delete=models.CASCADE, related_name="favorites")
