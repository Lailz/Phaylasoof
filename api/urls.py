from django.urls import path
from api import views
from api.views import (
    CategoryListView,
    AnswerListView,
    QuestionListView,

    UserRegisterView,
    LoginAPIView
    )

urlpatterns = [
    path('category_list/', CategoryListView.as_view(), name='api-category_list'),
    path('question_list/<int:category_id>/', QuestionListView.as_view(), name='api-question_list'),
    path('answer_list/<int:question_id>/', AnswerListView.as_view(), name='api-answer_list'),
    path('register/', UserRegisterView.as_view(), name='api-register'),
    path('login/', LoginAPIView.as_view(), name='api-login'),

]


'''
path('upvote/', UpvoteCreateView.as_view(), name='api-upvote'),
path('downvote/', DownvoteCreateView.as_view(), name='api-downvote'),

path('question_detail/<int:question_id>/q-upvote/', UpvoteCreateView.as_view(), name='api-q-upvote'),
path('question_detail/<int:question_id>/q-downvote/', DownvoteCreateView.as_view(), name='api-q-downvote'),

path('category_detail/<int:category_id>/', CategoryDetailView.as_view(), name='api-category_detail'),
path('question_detail/<int:question_id>/', QuestionDetailView.as_view(), name='api-question_detail'),
path('upvote/', UpvoteCreateView.as_view(), name='api-upvote'),
path('downvote/', DownvoteCreateView.as_view(), name='api-downvote'),

path('answer_detail/<int:answer_id>/', AnswerDetailView.as_view(), name='api-answer_detail'),

QuestionDetailView,

AnswerDetailView,
UpvoteCreateView,
DownvoteCreateView,

#CategoryDetailView,
'''
