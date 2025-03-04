from django.contrib import admin
from .models import User, Song



class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist")


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    filter_horizontal = ("songs",)  # Allows selecting songs in a multi-select widget
    filter_horizontal = ("matches",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Song, SongAdmin)



