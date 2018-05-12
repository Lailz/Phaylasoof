from django.db import models
from django.contrib.auth.models import User



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
    def __str__(self):
        return '{} follows {}'.format(self.follower, self.category)



class FollowQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return '{} follows {}'.format(self.follower, self.question)



class FollowUser(models.Model):
    #  will give me who I'm following
    following = models.ForeignKey(User, related_name="followings", on_delete=models.CASCADE)
    #  will give me who is following me
    follower = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    def __str__(self):
        return '{} follows {}'.format(self.follower, self.following)



class UpvoteQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self):
        return '{} upvotes {}'.format(self.user, self.question)

class DownvoteQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self):
        return '{} downvotes {}'.format(self.user, self.question)

class UpvoteAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    def __str__(self):
        return '{} upvotes {}'.format(self.user, self.answer)

class DownvoteAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    def __str__(self):
        return '{} downvotes {}'.format(self.user, self.answer)

class FeedPage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return 'FeedPage for user {}'.format(self.user.username)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    dob = models.DateField(auto_now=False, auto_now_add=False, null=True)
    biography = models.CharField(max_length=500)
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
