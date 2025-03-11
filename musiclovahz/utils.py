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
        .exclude(id__in=current_user.matches.all())     # exclude already matched users
        .exclude(id__in=current_user.likes.all())       # exclude profiles already liked
        .annotate(shared_songs=Count("songs", distinct=True))                                                           # adds a new field called shared_songs to each user in the queryset.
                                                                                                                        # count("songs", filter=...) → counts how many songs the user has
                                                                                                                        # filter=models.Q(songs__in=current_user.songs.all()) → Ensures we only count songs that match with current_user
                                                                                                                        # Q = query object
        .filter(shared_songs__gte=NUMBER_OF_MUTUAL_SONGS)                                                               # gte = predefined meaning greater than or equal to
        .order_by('id')  # ensure consistent order for pagination
    )

    # print(matching_users)
    return matching_users


def find_songs_in_common(current_user, matched_user):
    mutual_songs = (Song.objects
                    .filter(users=current_user)
                    .filter(users=matched_user)
                    .distinct())
    print(f"Songs in common function: {mutual_songs}")
    return mutual_songs if mutual_songs.exists() else []


# TODO returns the wrong songs, if you like 1 more song than your match it is a common liked song!!! (see above function)
def find_songs_in_common_for_matches(current_user):
    matches = (
        User.objects.filter(
            songs__in=current_user.songs.all()
        )
        .exclude(id=current_user.id)
        .annotate(shared_songs=Count("songs",
                                     distinct=True))
        .filter(shared_songs__gte=NUMBER_OF_MUTUAL_SONGS)
    )
    mutual_songs = Song.objects.filter(users__in=matches).filter(users=current_user).distinct()
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
    # find mutual likes (users that both like and are liked by the current user) but exclude matches
    mutual_likes = (User.objects
                    .filter(likes=current_user, liked_by=current_user)
                    .exclude(id__in=current_user.matches.all()))
    return mutual_likes


def smart_title_case(text):
    # This regex pattern will fix cases like "it's" by preserving the apostrophe
    return re.sub(r"(\w+('[a-zA-Z]+)?)", lambda m: m.group(0).capitalize(), text)
