from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserSignup, UserLogin

def usersignup(request):
    form = UserSignup()
    if request.method == 'POST':
        form = UserSignup(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            login(request, user)
            messages.success(request, "Successfully signed up!")
            return redirect("profile", pk=user.pk)
        messages.error(request, form.errors)
        return redirect("signup")
    context = {
        "form": form
    }
    return render(request, 'signup.html', context)

def usersignin(request):
    form = UserLogin()
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Successfully signed in!")
                return redirect('profile', pk=auth_user.pk)

            messages.error(request, "Wrong username/password combination. Please try again.")
            return redirect("signin")
        messages.error(request, form.errors)
        return redirect("signin")
    context = {
        "form": form
    }
    return render(request, 'signin.html', context)

def usersignout(request):
    logout(request)
    messages.success(request, "Successfully signed out!")
    return redirect("signin")
