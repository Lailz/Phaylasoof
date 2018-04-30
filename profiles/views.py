from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Follow, Post, Like
from django.http import JsonResponse

def profile(request, pk):
    if request.user.is_anonymous:
        return redirect('signin')

    if request.method == "POST":
        message = request.POST.get("message")
        Post.objects.create(user=request.user, message=message)
        messages.success(request, "New post generated for your followers!")

    context = {
        "user": User.objects.get(pk=pk)
    }
    return render(request, 'profile.html', context)

def search_users(request):
    if request.user.is_anonymous:
        return redirect('signin')

    following_list = []
    followings = request.user.follower.all()
    for following in followings:
        following_list.append(following.following)

    users = User.objects.none()

    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query)

    context = {
        "users":users,
        "following_list":following_list
    }
    return render(request, 'search_users.html', context)

def follow(request, pk):
    if request.user.is_anonymous:
        return redirect('signin')

    following = User.objects.get(pk=pk)
    follower = request.user

    follow, created = Follow.objects.get_or_create(follower=follower, following=following)
    if created:
        messages.success(request, "Successfully followed %s!"%(following))
    else:
        follow.delete()
        messages.success(request, "Unfollowed %s!"%(following))

    return redirect('search-users')

def followers(request, pk):
    if request.user.is_anonymous:
        return redirect('signin')

    user = request.user
    followers = user.following.all()
    context = {
        "followers": followers,
    }
    return render(request, 'followers.html', context)

def following(request, pk):
    if request.user.is_anonymous:
        return redirect('signin')

    user = request.user
    following = user.follower.all()
    context = {
        "following": following,
    }
    return render(request, 'following.html', context)

def feed(request):
    if request.user.is_anonymous:
        return redirect('signin')

    user = request.user
    following_list = []
    followings = request.user.follower.all()
    for following in followings:
        following_list.append(following.following)

    post_list = Post.objects.filter(
        Q(user__in=following_list)|
        Q(user=request.user)
        ).distinct()

    # like_list = []
    # favorites = user.favorite_set.all()
    # for fav in favorites:
    #     favorite_list.append(fav.post)

    like_list = user.like_set.all().values_list('post_id', flat=True)

    context = {
        "feed": post_list,
        "likes":like_list,
    }
    return render(request, 'feed.html', context)

def like(request, pk):
    post_object = Post.objects.get(pk=pk)
    new_like, created = Like.objects.get_or_create(user=request.user, post=post_object)

    if created:
        action="like"
    else:
        new_like.delete()
        action="unlike"

    response = {
        "action": action,
    }
    return JsonResponse(response, safe=False)
