"""Views for auctions app"""
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import User, ListingForm, Listing, Category, CommentForm, BidForm
from .util import set_listing_current_bid, create_listing_context


def index(request):
    """ Returns index page populated with listings from Listing db table """
    listings = set_listing_current_bid(Listing.objects.filter(is_active=True))
    return render(request, "auctions/index.html", {
        "listings": listings,
        "selected": "index"})


def category(request, category_id):
    """ Returns index page showing filtering Listings by passed Category """
    listings = set_listing_current_bid(Listing.objects.filter(category=category_id))
    return render(request, "auctions/index.html", {
        "listings": listings,
        "selected": "index",
        "category": get_object_or_404(Category, id=category_id)})


def categories(request):
    """ Returns categories page, showing all category items from Category db table """
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
        "selected": "categories"})


@login_required(login_url="/login")
def watchlist(request):
    """ Returns index page showing listing on user's watchlist"""
    listings = set_listing_current_bid(Listing.objects.filter(watchlist=request.user.id))
    return render(request, "auctions/index.html", {
        "listings": listings,
        "selected": "watchlist"})


def view_listing(request, listing_id):
    """ Returns individual listing view and process POST requests """
    listing = get_object_or_404(Listing, id=listing_id)
    # Prepare context dict. Used to pass data to template
    context = create_listing_context(request, listing)

    if request.method == "POST":
        # If user clicked watchlist button
        # we first have to check if user is authenticated, if not display message
        if "watchlist_submit" in request.POST:
            if not request.user.is_authenticated:
                context["message"] = "You need to be logged in to add / remove a list from watchlist."
                return render(request, "auctions/viewlisting.html", context)
            if not context["is_watchlisted"]:
                listing.watchlist.add(request.user)
            else:
                listing.watchlist.remove(request.user)
        # if user closes bid, we check first if the user is owner and if bid is active
        if "close_listing" in request.POST:
            if not context["is_owner"]:
                context["message"] = "You have to be the owner of the listing in order to be able to close it."
                return render(request, "auctions/viewlisting.html", context)
            if not listing.is_active:
                context["message"] = "This listing is already closed."
                return render(request, "auctions/viewlisting.html", context)
            listing.is_active = False
            listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    return render(request, "auctions/viewlisting.html", context)


def post_comment(request, listing_id):
    """ Posts a comment and returns the listing view """
    listing = get_object_or_404(Listing, id=listing_id)
    # Prepare context dict. Used to pass data to template
    context = create_listing_context(request, listing)

    # If user posted a comment, we check if comment can be posted
    # If so then we create new comment entry
    if request.method == "POST" and "post_comment" in request.POST:
        if not request.user.is_authenticated:
            context["message"] = "You need to be logged in to comment."
            return render(request, "auctions/viewlisting.html", context)
        if not listing.is_active:
            context["message"] = "You cannot post comments on a closed listing."
            return render(request, "auctions/viewlisting.html", context)
        new_comment = CommentForm(request.POST)
        new_comment = new_comment.save(commit=False)
        new_comment.author = request.user
        new_comment.item = listing
        new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def place_bid(request, listing_id):
    """ Places a bid on a listing """
    lipsting = get_object_or_404(Listing, id=listing_id)
    # Prepare context dict. used to pass data to template
    context = create_listing_context(request, listing)

    # If user places a bid
    if request.method == "POST" and "place_bid" in request.POST:
        if not request.user.is_authenticated:
            context["message"] = "You need to be logged in to place a bid."
            return render(request, "auctions/viewlisting.html", context)
        if not listing.is_active:
            context["message"] = "You cannot bid on a closed listing"
            return render(request, "auctions/viewlisting.html", context)
        amount = Decimal(request.POST.get("amount"))

        # We need to validate bid also on the server side
        # if there are no bids, the bid needs to be greater or equal
        # to initial bid. If there are bid, the bid needs to be greater
        # than last bid

        if context["bid_count"] == 0 and amount < listing.initial_bid:
            context["message"] = "Bid needs to be greater than initial bid"
            return render(request, "auctions/viewlisting.html", context)
        if context["bid_count"] != 0 and amount <= context["current_bid"]:
            context["message"] = "Bid needs to be greater than current bid"
            return render(request, "auctions/viewlisting.html", context)

        # If amount passes validation, then we post the bid
        bid = BidForm(request.POST)
        bid = bid.save(commit=False)
        bid.bidder = request.user
        bid.item = listing
        bid.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url="/login")
def create_listing(request):
    """ Creates listing via POST method """
    if request.method == "POST":
        new_listing = ListingForm(request.POST)
        # Save form without commiting so that current user is added as author
        # Technique source:
        # https://stackoverflow.com/questions/27192251/set-value-of-excluded-field-in-django-modelform-programmatically
        new_listing = new_listing.save(commit=False)
        new_listing.author = request.user
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/createlisting.html", {
        "form": ListingForm,
        "selected": "add"
        })


def login_view(request):
    """ Logs in user """
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
    """ Logs out user """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """ Creates user account """
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
