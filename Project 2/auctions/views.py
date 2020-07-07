from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, ListingForm, Listing

def index(request):
    return render(request, "auctions/index.html", { "listings" : Listing.objects.all(), "selected" : "index"})

def add_listing(request):
    if request.method == "POST":
        new_listing = ListingForm(request.POST)
        # save form without commiting so that current user is added as author
        # source: https://stackoverflow.com/questions/27192251/set-value-of-excluded-field-in-django-modelform-programmatically
        new_listing = new_listing.save(commit=False)
        new_listing.author = request.user
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/addlisting.html", { 
            "form" : ListingForm,
            "selected" : "add"
            })


def login_view(request):
    context = { "selected" : "login" }
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            context["message"] = "Invalid username and/or password."
            return render(request, "auctions/login.html", context)
    else:
        return render(request, "auctions/login.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    context = { "selected": "register" }
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            context["message"] = "Passwords must match."
            return render(request, "auctions/register.html", context)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
            user.save()
        except IntegrityError:
            context["message"] = "Username already taken."
            return render(request, "auctions/register.html", context)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", context)
