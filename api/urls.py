from django.urls import path
from api import views
from api.views import (
    QuestionListView,
    QuestionDetailView,
    CategoryListView,
    CategoryDetailView,
    UpvoteCreateView,
    DownvoteCreateView,
    UserRegisterView,
    LoginAPIView
    )

urlpatterns = [
    path('question_list/', QuestionListView.as_view(), name='api-question_list'),
    path('question_detail/<int:question_id>/', QuestionDetailView.as_view(), name='api-question_detail'),
    path('category_list/', CategoryListView.as_view(), name='api-category_list'),
    path('category_detail/<int:category_id>/', CategoryDetailView.as_view(), name='api-category_detail'),
    path('upvote/', UpvoteCreateView.as_view(), name='api-upvote'),
    path('downvote/', UpvoteCreateView.as_view(), name='api-downvote'),
    path('register/', UserRegisterView.as_view(), name='api-register'),
    path('login/', LoginAPIView.as_view(), name='api-login'),

]
