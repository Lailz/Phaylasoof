from django.urls import path
from api import views
from api.views import (
    CategoryListView,
    AnswerListView,
    QuestionListView,
    UpvoteCreateView,
    DownvoteCreateView,
    UserRegisterView,
    LoginAPIView,
    FollowCategoryCreateView,
    FollowUserCreateView
    )

urlpatterns = [
    path('category_list/', CategoryListView.as_view(), name='api-category_list'),
    path('question_list/<int:category_id>/', QuestionListView.as_view(), name='api-question_list'),
    path('answer_list/<int:question_id>/', AnswerListView.as_view(), name='api-answer_list'),
    path('register/', UserRegisterView.as_view(), name='api-register'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('question_list/<int:category_id>/follow-category/', FollowCategoryCreateView.as_view(), name='api-follow-category'),
    path('follow-user/<int:user_id>/follow-user/', FollowUserCreateView.as_view(), name='api-follow-user'),
    path('answer_list/<int:question_id>/upvote/', UpvoteCreateView.as_view(), name='api-upvote-question'),
    path('answer_list/<int:question_id>/downvote/', DownvoteCreateView.as_view(), name='api-downvote-question'),
]
