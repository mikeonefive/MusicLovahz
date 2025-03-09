from django import forms
from .models import User, Song
from django.contrib.auth.forms import UserCreationForm


# for updating the picture and putting in songs
class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "profile_picture"]

    def clean_songs(self):
        songs = self.cleaned_data.get("songs")
        if len(songs) > 10:
            raise forms.ValidationError("You can only have up to 10 songs in your profile.")
        return songs


class CustomUserCreationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)  # allow users to upload a profile picture

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']
