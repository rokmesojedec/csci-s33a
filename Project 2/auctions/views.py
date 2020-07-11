from django.contrib.auth import authenticate, login, logout
from decimal import *
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.urls import reverse
from .models import User, ListingForm, Listing, Category, CommentForm, Comment, BidForm

def index(request):
    """Returns index page populated with listings from Listing db table """
    listings = get_list_or_404(Listing)
  
    return render(request, "auctions/index.html", {
        "listings" : get_list_or_404(Listing),
        "selected" : "index"})


def category(request, category_id):
    """ Returns index page showing filtering Listings by passed Category """
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(categories=category_id),
        "selected" : "index",
        "category": get_list_or_404(Category, id=category_id)})


def categories(request):
    """ Returns categories page, showing all category items from Category db table """
    return render(request, "auctions/categories.html", {
        "categories" : Category.objects.all(),
        "selected" : "categories"})


def watchlist(request):
    """ Returns index page showing listing on user's watchlist"""
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(wishlist=request.user.id),
        "selected" : "watchlist"})


def view_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    comments = Comment.objects.filter(item=listing, author=request.user)
    is_watchlisted = len(request.user.wishlist_user.filter(id=listing_id)) > 0
    if request.method == "POST":
        if "watchlist_submit" in request.POST and not is_watchlisted:
            listing.wishlist.add(request.user)
        else:
            listing.wishlist.remove(request.user)
        if "post_comment" in request.POST:
            new_comment = CommentForm(request.POST)
            new_comment = new_comment.save(commit=False)
            new_comment.author = request.user
            new_comment.item = listing
            new_comment.save()
        if "place_bid" in request.POST:
            bid = BidForm(request.POST)
            bid = bid.save(commit=False)
            bid.bidder = request.user
            bid.item = listing
            bid.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    print(dir(BidForm.helper.layout[0]), BidForm.helper.layout[0])
    BidForm.helper.layout[0].attrs['min'] = listing.initial_bid + Decimal(0.01)
    return render(request, "auctions/viewlisting.html", {
        "listing" : listing,
        "comment_form" : CommentForm,
        "comments" : comments,
        "bid_form" : BidForm,
        "watchlist_value" : ("Add to Watchlist", "Remove from Watchlist")[is_watchlisted]
    })


def add_listing(request):
    if request.method == "POST":
        new_listing = ListingForm(request.POST)
        # save form without commiting so that current user is added as author
        # source: https://stackoverflow.com/questions/27192251/set-value-of-excluded-field-in-django-modelform-programmatically
        new_listing = new_listing.save(commit=False)
        new_listing.author = request.user
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/addlisting.html", {
        "form" : ListingForm,
        "selected" : "add"
        })


def login_view(request):
    context = {"selected": "login"}
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        context["message"] = "Invalid username and/or password."
        return render(request, "auctions/login.html", context)

    return render(request, "auctions/login.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    context = {"selected": "register"}
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
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=firstname,
                last_name=lastname)
            user.save()
        except IntegrityError:
            context["message"] = "Username already taken."
            return render(request, "auctions/register.html", context)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/register.html", context)
