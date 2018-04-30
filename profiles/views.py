from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Follow, Clue, Favorite
from django.http import JsonResponse

def profile(request, pk):
    if request.user.is_anonymous:
        return redirect('signin')

    if request.method == "POST":
        message = request.POST.get("message")
        Clue.objects.create(user=request.user, message=message)
        messages.success(request, "New clue generated for your stalkers!")

    context = {
        "user": User.objects.get(pk=pk)
    }
    return render(request, 'profile.html', context)

def search_users(request):
    if request.user.is_anonymous:
        return redirect('signin')

    prey_list = []
    preys = request.user.stalker.all()
    for prey in preys:
        prey_list.append(prey.prey)

    users = User.objects.none()

    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query)

    context = {
        "users":users,
        "prey_list":prey_list
    }
    return render(request, 'search_users.html', context)

def follow(request, pk):
    if request.user.is_anonymous:
        return redirect('signin')

    prey = User.objects.get(pk=pk)
    stalker = request.user

    follow, created = Follow.objects.get_or_create(stalker=stalker, prey=prey)
    if created:
        messages.success(request, "Successfully followed %s!"%(prey))
    else:
        follow.delete()
        messages.success(request, "Unfollowed %s!"%(prey))

    return redirect('search-users')

def followers(request, pk):
    if request.user.is_anonymous:
        return redirect('signin')

    user = request.user
    followers = user.prey.all()
    context = {
        "followers": followers,
    }
    return render(request, 'followers.html', context)

def following(request, pk):
    if request.user.is_anonymous:
        return redirect('signin')

    user = request.user
    following = user.stalker.all()
    context = {
        "following": following,
    }
    return render(request, 'following.html', context)

def feed(request):
    if request.user.is_anonymous:
        return redirect('signin')

    user = request.user
    prey_list = []
    preys = request.user.stalker.all()
    for prey in preys:
        prey_list.append(prey.prey)

    clue_list = Clue.objects.filter(
        Q(user__in=prey_list)|
        Q(user=request.user)
        ).distinct()

    # favorite_list = []
    # favorites = user.favorite_set.all()
    # for fav in favorites:
    #     favorite_list.append(fav.clue)

    favorite_list = user.favorite_set.all().values_list('clue_id', flat=True)

    context = {
        "feed": clue_list,
        "favorites":favorite_list,
    }
    return render(request, 'feed.html', context)

def favorite(request, pk):
    clue_object = Clue.objects.get(pk=pk)
    new_favorite, created = Favorite.objects.get_or_create(user=request.user, clue=clue_object)

    if created:
        action="favorite"
    else:
        new_favorite.delete()
        action="unfavorite"

    response = {
        "action": action,
    }
    return JsonResponse(response, safe=False)
