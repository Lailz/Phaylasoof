from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.profile, name='profile'),
    path('search/', views.search_users, name='search-users'),
    path('follow/<int:pk>/', views.follow, name='follow'),
    path('followers/<int:pk>/', views.followers, name='followers'),
    path('following/<int:pk>/', views.following, name='following'),
    path('feed/', views.feed, name='feed'),
    path('like/<int:pk>/', views.like, name='like'),
]
