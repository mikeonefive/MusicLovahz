import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404

from .forms import CustomUserCreationForm, UserProfileForm
from .models import User, Song, Message

from .utils import check_mutual_like_and_update_data, convert_to_smart_title_case, find_users_by_songs

import yt_dlp


def login_view(request):
    if request.method == "POST":
        # attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # check if authentication successful
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
            user = form.save()                      # automatically saves all fields, including profile_picture
            login(request, user)
            return redirect("index")                # redirect after successful registration
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, "musiclovahz/register.html", {"form": form})


def index(request):
    if request.user.is_authenticated:
        return render(request, "musiclovahz/show_profiles.html")
    else:
        return render(request, "musiclovahz/login.html")


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)      # makes sure the form is pre-filled with the current user's info

        titlesList = request.POST.getlist("title")
        artistList = request.POST.getlist("artist")

        if form.is_valid():
            # save the user profile, excluding the songs field
            updated_user = form.save(commit=False)  # save without committing to database yet
            updated_user.save()                     # save the user object first

            for title, artist in zip(titlesList, artistList):   # ZIP = built-in function that combines multiple iterables (such as lists, tuples)
                                                                # into an iterator of tuples
                                                                # each tuple contains the elements from each iterable at the same index, it "zips" the iterables together based on their positions
                                                                # Title: Song 1, Artist: Artist 1
                title = convert_to_smart_title_case(title.strip())
                artist = artist.upper().strip()

                # if user entered a song, add it to their profile
                if title and artist:
                    song, was_newly_added = Song.objects.get_or_create(title=title, artist=artist)  # if song exists, it won’t duplicate; if not, it creates a new one
                    # new_song, created = Song.objects.get_or_create(title=title, artist=artist) created stores a boolean if we created a new song or if it was retrieved from the database
                    user.songs.add(song)    # add song to user's profile


            return redirect("index")                                   # Redirect after saving, outside the for loop

    else:
        form = UserProfileForm(instance=user)                          # pre-fill with existing user data

    return render(request, "musiclovahz/edit_profile.html", {
        "form": form
    })


@login_required
def find_matching_profiles_API(request):
    current_user = request.user
    # find users who have songs in common with current_user
    song_mates = find_users_by_songs(current_user)

    # convert data for JSON response
    profiles_data = [user.serialize(current_user) for user in song_mates]

    return JsonResponse({
        "profiles": profiles_data
    })


@login_required
def show_matches(request):
    current_user = request.user
    all_matches = current_user.matches.all()

    # convert data for JSON response
    profiles_data = [user.serialize(current_user) for user in all_matches]

    return JsonResponse({
        "profiles": profiles_data
    })


@login_required
def like_unlike_profile(request, user_id):
    loggedin_user = request.user

    # get the profile by id
    profile_to_update = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        # check if user already likes profile -> do nothing
        if loggedin_user.likes.filter(id=user_id).exists():
            return JsonResponse({}, status=400)

        # update database
        loggedin_user.likes.add(profile_to_update)

        # check if like is mutual and update data if necessary
        if check_mutual_like_and_update_data(loggedin_user):
            return JsonResponse({"message": f"You and {profile_to_update.username} like each other"}, status=201)

        return JsonResponse({"message": f"You like {profile_to_update.username}"}, status=201)
        # return JsonResponse({}, status=201)           # 201 = new resource created by server

    elif request.method == "DELETE":
        # update database
        loggedin_user.likes.remove(profile_to_update)
        loggedin_user.unlikes.add(profile_to_update)
        loggedin_user.matches.remove(profile_to_update)
        profile_to_update.matches.remove(loggedin_user)

        return JsonResponse({"message": f"You don't like {profile_to_update.username}"}, status=200)
        # return JsonResponse({}, status=200)     # empty JSON response ok

    return JsonResponse({"error": "Invalid request method"},
                        status=405)


@login_required
def get_messages(request, chatpartner_id):
    current_user = request.user
    chat_partner = get_object_or_404(User, id=chatpartner_id)

    messages = Message.objects.filter(
        Q(sender=current_user, recipient=chat_partner) |
        Q(sender=chat_partner, recipient=current_user)
    ).order_by("timestamp")

    # mark unread messages as read when the recipient views them
    unread_messages = messages.filter(recipient=current_user, read=False)
    unread_messages.update(read=True)

    # messages_data = [message.serialize() for message in messages]
    messages_data = []
    for message in messages:
        messages_data.append(message.serialize())

    return JsonResponse({"messages": messages_data},
                        status=200)


@login_required
def send_message(request, chatpartner_id):
    sender = request.user
    recipient = get_object_or_404(User, id=chatpartner_id)

    # composing a new message must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    # get contents of email or default to empty
    content = data.get("content", "").strip()
    if not content or not sender or not recipient:
        return JsonResponse({"error": "Message cannot be empty and/or needs a sender and recipient."},
                            status=400)

    # create a new message and save it in database
    message = Message.objects.create(sender=sender,
                      recipient=recipient,
                      content=content)
    message.save()

    return JsonResponse(message.serialize(),
                        status=201)


def get_audio_url(request):
    query = request.GET.get("query", "")

    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)

    ydl_opts = {"quiet": True,
                "default_search": "ytsearch1",
                "format": "bestaudio[ext=m4a]/best",
                "noplaylist": True,
                "extractaudio": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # fetch the video/audio info
            info = ydl.extract_info(query, download=False)
            audio_url = info["entries"][0]["url"]  # get the best audio stream URL, first entry in the list of media
        except Exception as e:
            # in case something goes wrong (invalid query or no result)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"audio_url": audio_url})
