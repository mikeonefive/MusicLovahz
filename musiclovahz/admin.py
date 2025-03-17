from django.contrib import admin
from .models import User, Song, Message



class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist")


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    filter_horizontal = ("songs", "likes", "unlikes", "matches")  # Allows selecting songs in a multi-select widget


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "serialize")


admin.site.register(User, CustomUserAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Message, MessageAdmin)
