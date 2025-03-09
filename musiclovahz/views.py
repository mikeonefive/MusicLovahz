from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from .forms import CustomUserCreationForm, UserProfileForm
from .models import User, Song
import json

from .utils import update_matches, get_users_who_like_each_other, find_songs_in_common, \
    smart_title_case, find_songs_in_common_for_matches, find_users_by_songs


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
        return find_matching_profiles(request)
    else:
        return render(request, "musiclovahz/login.html")


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)      # makes sure the form is pre-filled with the current user's info

        title = smart_title_case(request.POST.get("title").strip())             # get title from form
        artist = request.POST.get("artist").upper().strip()                     # get artist name from form

        if form.is_valid():
            # save the user profile, excluding the songs field
            updated_user = form.save(commit=False)  # save without committing to database yet
            updated_user.save()                     # save the user object first

            # if user entered a song, add it to their profile
            if title and artist:
                song, was_newly_added = Song.objects.get_or_create(title=title, artist=artist)  # if song exists, it won’t duplicate; if not, it creates a new one
                # new_song, created = Song.objects.get_or_create(title=title, artist=artist) created stores a boolean if we created a new song or if it was retrieved from the database
                user.songs.add(song)  # Add song to user's profile

            return redirect("index")

    else:
        form = UserProfileForm(instance=user)                                  # pre-fill with existing user data

    return render(request, "musiclovahz/edit_profile.html", {
        "form": form
    })


@login_required
def find_matching_profiles(request):
    current_user = request.user
    # find users who have songs in common with current_user
    song_mates = find_users_by_songs(current_user)

    # find out which songs they have in common
    songs_in_common = find_songs_in_common(current_user)

    # split into pages with Paginator
    # paginator = Paginator(song_mates, 1)  # show 1 profile per page
    # page_number = request.GET.get('page')
    # current_page = paginator.get_page(page_number)

    # print(f"Found {len(song_mates)} song mates")

    # if 2 users have songs in common, check if they like each other and if so update database
    if song_mates:
        check_mutual_like_and_update_data(request, current_user, songs_in_common)

    # print(f"Matches being passed to template: {song_mates}")

    return render(request, "musiclovahz/show_profiles.html", {
        "matches": song_mates,
        "songs_in_common": songs_in_common
    })

    # convert users to a list of dicts for JSON response
    # mutual_like_list = list(users_that_like_each_other.values("id", "username"))
    # return JsonResponse({"users_that_like_each_other": mutual_like_list})


def check_mutual_like_and_update_data(request, current_user,songs_in_common):
    users_that_like_each_other = get_users_who_like_each_other(current_user)
    # print(f"users like each other: {users_that_like_each_other} & {current_user}")

    if users_that_like_each_other.exists():  # exists is more efficient because it doesn't get all the data
        # print(f"Mutual likes exist, updating matches.")

        update_matches(current_user, users_that_like_each_other)

        # # show the matches page
        # return render(request, "musiclovahz/show_profiles.html", {
        #     "matches": users_that_like_each_other,
        #     "songs_in_common": songs_in_common
        # })


@login_required
def show_matches(request):
    current_user = request.user
    songs_in_common = find_songs_in_common_for_matches(current_user)

    # print(current_user.matches.all())

    return render(request, "musiclovahz/show_profiles.html", {
        "matches": current_user.matches.all(),
        "songs_in_common": songs_in_common
    })


@csrf_exempt
@login_required
def like_unlike_profile(request, user_id):
    loggedin_user = request.user

    # get the profile by id
    profile_to_update = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        # check if user already likes profile -> do nothing
        if loggedin_user.likes.filter(id=user_id).exists():
            return JsonResponse({"user_id": user_id, "liked" : f"already liked {user_id}"}, status=400)

        loggedin_user.likes.add(profile_to_update)
        return JsonResponse({"user_id": user_id, "liked": f"{profile_to_update}"})


    elif request.method == "DELETE":

        loggedin_user.likes.remove(profile_to_update)
        loggedin_user.matches.remove(profile_to_update)
        profile_to_update.matches.remove(loggedin_user)

        return JsonResponse({"unliked": f"{profile_to_update} {user_id}"})

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


