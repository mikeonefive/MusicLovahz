
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("find_matching_profiles", views.find_matching_profiles, name="find_matching_profiles"),
    path("show_matches", views.show_matches, name="show_matches")
]
