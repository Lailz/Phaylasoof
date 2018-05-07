from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.OneToOneField(User , on_delete=models.CASCADE)
	user_pic = models.ImageField()
	user_biography = models.TextField(max_length=300, null=True)


class Category(models.Model):
    category_title = models.CharField(max_length=255)
    category_description = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.category_title

    class Meta:
        ordering = ['-timestamp']


class Question(models.Model):
    question_content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_content

    class Meta:
        ordering = ['-timestamp']

class Answer(models.Model):
    answer_content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_content

    class Meta:
        ordering = ['-timestamp']

class FollowCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)



class FollowQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)



class FollowUser(models.Model):
    #  will give me who I'm following
    follower = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    #  will give me who is following me
    following = models.ForeignKey(User, related_name="followings", on_delete=models.CASCADE)



class Upvote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Downvote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
