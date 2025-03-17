from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    songs = models.ManyToManyField("Song", related_name="users", blank=True)

    likes = models.ManyToManyField("self",
                                   symmetrical=False,              # allows unidirectional relationships (e.g., A likes B, but B may not like A)
                                   related_name="liked_by",
                                   blank=True)

    unlikes = models.ManyToManyField("self",
                                   symmetrical=False,
                                   related_name="unliked_by",
                                   blank=True)

    matches = models.ManyToManyField("self",
                                    blank=True, symmetrical=True)  # `symmetrical=True` ensures bidirectional relationships

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # def clean(self):
    #     if self.matches.filter(id=self.id).exists():
    #         raise ValidationError("You cannot like yourself.")
    #
    # def save(self, *args, **kwargs):
    #     self.clean()  # Ensure validation runs on save
    #     super().save(*args, **kwargs)

    def __str__(self):
        return (f"username: {self.username},"
                f"id: {self.id}")

    def serialize(self, matched_user):
        from .utils import find_songs_in_common                         # import inside method to avoid circular imports

        songs_in_common = find_songs_in_common(self, matched_user)      # call the helper function here so the view is way cleaner

        return {
            "id": self.id,
            "username": self.username,
            "profile_picture": self.profile_picture.url if self.profile_picture else None,
            "songs": [song.serialize() for song in self.songs.all()],
            "likes": [like.id for like in self.likes.all()],
            "unlikes": [unlike.id for unlike in self.unlikes.all()],
            "matches": [match.id for match in self.matches.all()],
            "songs_in_common": [{"title": song.title, "artist": song.artist} for song in songs_in_common],
        }


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)

    def __str__(self):
        return (f"title: {self.title},"
                f"artist: {self.artist}")

    def serialize(self):
        return {
            "title": self.title,
            "artist": self.artist
        }


class Message(models.Model):
    sender = models.ForeignKey("User", on_delete=models.SET_NULL, related_name="messages_sent", null=True)
    recipient = models.ForeignKey("User", on_delete=models.SET_NULL,  related_name="messages_received", null=True)
    content = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def serialize(self):
        return {
            "sender": self.sender.username,
            "recipient" : self.recipient.username,
            "content": self.content,
            "datetime": self.timestamp.strftime('%B %d, %Y %I:%M %p'),
            "read": self.read
        }
