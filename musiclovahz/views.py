from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from .models import User
import json


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "musiclovahz/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "musiclovahz/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "musiclovahz/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "musiclovahz/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "musiclovahz/register.html")


def index(request):

    if request.user.is_authenticated:
        return find_matching_profiles(request)
    else:
        return render(request, "musiclovahz/login.html")


@login_required
def find_matching_profiles(request):
    current_user = request.user
    # print(current_user.songs.all())

    # Find users who have any song in common with current_user, but exclude current_user
    matching_user = User.objects.filter(songs__in=current_user.songs.all()).exclude(id=current_user.id)

    return render(request, "musiclovahz/show_profiles.html", {
        "matches": matching_user
    })


@login_required
def show_matches(request):
    current_user = request.user

    return render(request, "musiclovahz/show_profiles.html", {
        "matches": current_user.matches.all()
    })