from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit_profile", views.edit_profile, name="edit_profile"),

    path("find_matching_profiles", views.find_matching_profiles_and_update, name="find_matching_profiles"),
    path("show_matches", views.show_matches, name="show_matches"),
    path("check_mutual_likes", views.get_users_who_like_each_other, name="check_mutual_likes")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
