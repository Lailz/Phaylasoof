from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_title = models.CharField(max_length=255)
    category_description = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)
    class Meta:
        ordering = ['-timestamp']

class Question(models.Model):
    question_content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']

class Answer(models.Model):
    answer_content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']



class Upvote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Downvote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)

'''class Follow(models.Model):
    #  will give me who I'm following
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    #  will give me who is following me
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
'''
