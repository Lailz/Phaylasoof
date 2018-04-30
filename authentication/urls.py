from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.usersignup, name='signup'),
    path('signin/', views.usersignin, name='signin'),
    path('signout/', views.usersignout, name='signout'),
]
