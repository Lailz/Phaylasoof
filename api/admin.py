from django.contrib import admin
from .models import (
    Category,
    Question,
    Answer,
    UpvoteQuestion,
    DownvoteQuestion,
    UpvoteAnswer,
    DownvoteAnswer,
    FollowCategory,
    FollowUser,
    Profile,
    FollowQuestion,
    # FeedPage
)

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UpvoteQuestion)
admin.site.register(DownvoteQuestion)
admin.site.register(UpvoteAnswer)
admin.site.register(DownvoteAnswer)
admin.site.register(FollowCategory)
admin.site.register(FollowQuestion)
admin.site.register(FollowUser)
admin.site.register(Profile)
# admin.site.register(FeedPage)
