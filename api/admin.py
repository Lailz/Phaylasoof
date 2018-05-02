from django.contrib import admin
from .models import Question, Category, Upvote, Downvote

admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Upvote)
admin.site.register(Downvote)
