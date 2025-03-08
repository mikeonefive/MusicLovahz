from django.db.models import Count
from .models import User, Song
import re

# CONSTANTS
NUMBER_OF_MUTUAL_SONGS = 3

def find_users_by_songs(current_user):
    # matching_users = (User.objects.filter(
    #     songs__in=current_user.songs.all())
    #     .exclude(id=current_user.id)
    #     .exclude(id__in=current_user.matches.all()))  # exclude already matched users
    #
    # return matching_users

    matching_users = (
        User.objects.filter(
            songs__in=current_user.songs.all()
        )
        .exclude(id=current_user.id)
        .exclude(id__in=current_user.matches.all())  # exclude already matched users
        .annotate(shared_songs=Count("songs", distinct=True))                                                           # Adds a new field called shared_songs to each user in the queryset.
                                                                                                                        # Count("songs", filter=...) → Counts how many songs the user has.
                                                                                                                        # filter=models.Q(songs__in=current_user.songs.all()) → Ensures we only count songs that match with current_user
                                                                                                                        # Q = query object
        .filter(shared_songs__gte=NUMBER_OF_MUTUAL_SONGS)  # change this number if you want at least 3 common songs
    )

    return matching_users


def find_songs_in_common(current_user):
    matching_users = find_users_by_songs(current_user)
    mutual_songs = Song.objects.filter(users__in=matching_users).filter(users=current_user).distinct()
    return mutual_songs if mutual_songs.exists() else []


def update_matches(current_user, mutual_likes):
    current_user.matches.add(*mutual_likes)  # unpack queryset and add matches to the profile
    current_user.save()

    # add current_user to all matching users' matches
    for user in mutual_likes:
        user.matches.add(current_user)
        user.save()  # save each user after adding current_user to their matches

    # print(f"{current_user.matches} matches with {matching_users}")


def get_users_who_like_each_other(current_user):
    # find mutual likes (users that both like and are liked by the current user)
    mutual_likes = User.objects.filter(likes=current_user, liked_by=current_user)
    return mutual_likes


def smart_title_case(text):
    # This regex pattern will fix cases like "it's" by preserving the apostrophe
    return re.sub(r"(\w+('[a-zA-Z]+)?)", lambda m: m.group(0).capitalize(), text)
