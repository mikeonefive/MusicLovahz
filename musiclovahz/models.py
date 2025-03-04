from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    songs = models.ManyToManyField("Song", related_name="users")

    matches = models.ManyToManyField("self",
                                        symmetrical=False,  # allows unidirectional relationships (e.g., A likes B, but B may not like A),
                                        related_name="matched_by")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "songs": [song.serialize() for song in self.songs.all()],
            "matches": [match.serialize() for match in self.matches.all()]
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
