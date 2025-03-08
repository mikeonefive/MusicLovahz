from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from .forms import CustomUserCreationForm
from .models import User
import json

from .utils import update_matches, get_users_who_like_each_other, find_users_by_songs, find_songs_in_common


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
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # handles file uploads too
        if form.is_valid():
            user = form.save()  # automatically saves all fields, including profile_picture
            login(request, user)
            return redirect("index")  # redirect after successful registration
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, "musiclovahz/register.html", {"form": form})


def index(request):
    if request.user.is_authenticated:
        return find_matching_profiles_and_update(request)
    else:
        return render(request, "musiclovahz/login.html")


@login_required
def find_matching_profiles_and_update(request):
    current_user = request.user

    # find users who have songs in common with current_user
    song_mates = find_users_by_songs(current_user)

    # find out which songs they have in common
    songs_in_common = find_songs_in_common(current_user)

    # split posts into pages with Paginator
    paginator = Paginator(song_mates, 1)  # show 1 profile per page
    page_number = request.GET.get('page')
    current_page = paginator.get_page(page_number)

    # if 2 users have songs in common, check if they like each other and update database
    if song_mates:
        users_that_like_each_other = get_users_who_like_each_other(current_user)

        if users_that_like_each_other:
            update_matches(current_user, users_that_like_each_other)
            # show the matches page
            return render(request, "musiclovahz/show_profiles.html", {
                "matches": users_that_like_each_other,
                "songs_in_common": songs_in_common
            })

    return render(request, "musiclovahz/show_profiles.html", {
        "matches": current_page,
        "songs_in_common": songs_in_common
    })

    # convert users to a list of dicts for JSON response
    # mutual_like_list = list(users_that_like_each_other.values("id", "username"))
    # return JsonResponse({"users_that_like_each_other": mutual_like_list})


@login_required
def show_matches(request):
    current_user = request.user
    songs_in_common = find_songs_in_common(current_user)

    return render(request, "musiclovahz/show_profiles.html", {
        "matches": current_user.matches.all(),
        "songs_in_common": songs_in_common
    })