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
    FollowQuestionCreateView,
    FollowUserCreateView,
    QuestionCreateView,
    QuestionDeleteView,
    AnswerCreateView,
    AnswerDeleteView,
    FollowCategoryListView,
    FollowQuestionListView
    )

urlpatterns = [
    path('category/list/', CategoryListView.as_view(), name='api-category_list'),
    path('question/list/<int:category_id>/', QuestionListView.as_view(), name='api-question_list'),
    path('question/create/', QuestionCreateView.as_view(), name='api-question-create'),
    path('question/delete/<int:question_id>/', QuestionDeleteView.as_view(), name='api-question-delete'),
    path('answer/list/<int:question_id>/', AnswerListView.as_view(), name='api-answer_list'),
    path('answer/create/', AnswerCreateView.as_view(), name='api-answer-create'),
    path('answer/delete/<int:answer_id>/', AnswerDeleteView.as_view(), name='api-answer-delete'),
    path('register/', UserRegisterView.as_view(), name='api-register'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('follow/category/', FollowCategoryCreateView.as_view(), name='api-follow-category'),
    path('follow/category/list/<int:category_id>/', FollowCategoryListView.as_view(), name='api-follow-category-list'),
    path('follow/question/', FollowQuestionCreateView.as_view(), name='api-follow-question'),
    path('follow/question/list/<int:question_id>/', FollowQuestionListView.as_view(), name='api-follow-question-list'),
    path('follow/user/', FollowUserCreateView.as_view(), name='api-follow-user'),
    path('answer/list/<int:question_id>/upvote/', UpvoteCreateView.as_view(), name='api-upvote-question'),
    path('answer/list/<int:question_id>/downvote/', DownvoteCreateView.as_view(), name='api-downvote-question'),

]
