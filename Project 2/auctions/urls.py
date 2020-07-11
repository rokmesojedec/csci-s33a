from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/<str:category_id>", views.category, name="category"),
    path("categories", views.categories, name="categories"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<str:listing_id>", views.view_listing, name="listing"),
    path("comment/<str:listing_id>", views.post_comment, name="comment"),
    path("bid/<str:listing_id>", views.place_bid, name="bid"),
]
