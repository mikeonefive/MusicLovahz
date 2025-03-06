
from django.db.models import Count
from .models import User
from ..project5.settings import NUMBER_OF_MUTUAL_SONGS


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
        .distinct()
    )

    return matching_users


def update_matches(current_user, matching_users):
    current_user.matches.add(*matching_users)  # unpack queryset and add matches to the profile
    current_user.save()

    # add current_user to all matching users' matches
    for user in matching_users:
        user.matches.add(current_user)
        user.save()  # save each user after adding current_user to their matches

    # print(f"{current_user.matches} matches with {matching_users}")


def get_mutual_likes(current_user):
    # find mutual likes (users that both like and are liked by the current user)
    mutual_likes = current_user.likes.filter(liked_by=current_user)                 # return User.objects.filter(likes=current_user, liked_by=current_user)
    return mutual_likes
