from django.contrib import admin
from .models import User, Song



class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist")


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    filter_horizontal = ("songs", "likes", "unlikes", "matches")  # Allows selecting songs in a multi-select widget


admin.site.register(User, CustomUserAdmin)
admin.site.register(Song, SongAdmin)



