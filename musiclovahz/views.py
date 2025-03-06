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

from .utils import update_matches, get_mutual_likes, find_users_by_songs


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
        return find_matching_profiles_and_update(request)
    else:
        return render(request, "musiclovahz/login.html")


@login_required
def find_matching_profiles_and_update(request):
    current_user = request.user
    mutual_likes = None

    # find users who have songs in common with current_user
    song_mates = find_users_by_songs(current_user)

    # if 2 users have songs in common, check if they like each other and update database
    if song_mates:
        mutual_likes = get_mutual_likes(current_user)

        if mutual_likes:
            update_matches(current_user, song_mates)

    return render(request, "musiclovahz/show_profiles.html", {
        "matches": mutual_likes
    })

    # convert users to a list of dicts for JSON response
    # mutual_like_list = list(mutual_likes.values("id", "username"))
    # return JsonResponse({"mutual_likes": mutual_like_list})


@login_required
def show_matches(request):
    current_user = request.user
    return render(request, "musiclovahz/show_profiles.html", {
        "matches": current_user.matches.all()
    })