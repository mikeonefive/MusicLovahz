from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


# for updating the picture?
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'profile_picture']


class CustomUserCreationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)  # Allow users to upload a profile picture (optional)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']  # Add any other fields you want in registration