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
    path("add/", views.add_listing, name="add_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<str:listing_id>", views.view_listing, name="listing")
]
