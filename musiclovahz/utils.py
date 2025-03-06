
def update_matches(current_user, matching_users):

    current_user.matches.add(*matching_users)  # unpack queryset and add matches to the profile
    current_user.save()

    # add current_user to all matching users' matches
    for user in matching_users:
        user.matches.add(current_user)
        user.save()  # Save each user after adding current_user to their matches

    print(f"{current_user.matches} matches with {matching_users}")


def check_mutual_likes(current_user):

    # find mutual likes (users that both like and are liked by the current user)
    mutual_likes = current_user.likes.filter(liked_by=current_user)

    print(mutual_likes)


