from django.urls import path

from . import views

app_name = "encyclopedia"
# wiki/ endpoint is used to fetch a rendom entry
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.random_entry, name="random"),
    path("wiki/<str:entry_title>", views.entry, name="entry"),
    path("edit/<str:entry_title>", views.edit, name="edit"),
    path("add/", views.add, name="add")
]
