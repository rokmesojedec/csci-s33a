
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("posts/<int:post_id>", views.posts_edit, name="post_link"),
    path("edit/<int:post_id>", views.can_edit_post, name="can_edit_post"),
    path("like/<int:post_id>", views.like, name="like"),
    path("user/<int:user_id>", views.user, name="user"),
    path("user/<int:user_id>/follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("user/<int:user_id>/followers", views.followers_count, name="followers")
    ]
