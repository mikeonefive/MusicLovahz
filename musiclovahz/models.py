from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    songs = models.ManyToManyField("Song", related_name="users", blank=True)

    likes = models.ManyToManyField("self",
                                   symmetrical=False,       # allows unidirectional relationships (e.g., A likes B, but B may not like A)
                                   related_name="liked_by",
                                   blank=True)

    matches = models.ManyToManyField("self",
                                    blank=True)

    def clean(self):
        if self.matches.filter(id=self.id).exists():
            raise ValidationError("You cannot like yourself.")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation runs on save
        super().save(*args, **kwargs)

    def __str__(self):
        return f"username: {self.username}"
                # f"songs: {[song.serialize() for song in self.songs.all()]}")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "songs": [song.serialize() for song in self.songs.all()],
            "likes": [like.serialize() for like in self.likes.all()],
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
