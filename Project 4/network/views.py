import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, PostForm

PAGE_POST_LIMIT = 10


def process_posts(posts, request):
    """ Helper function for adding metadata to posts list """
    for post in posts:
        post.like_count = post.likes.count()
        post.like_label = ("Like", "Unlike")[request.user in post.likes.all()]
        post.can_edit = request.user == post.author

    paginator = Paginator(posts, PAGE_POST_LIMIT)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    """ Gets all posts """
    posts = process_posts(Post.objects.all().order_by("-created"), request)
    return render(
        request,
        "network/index.html",
        {"page_obj": posts, "selected": "index", "form": PostForm},
    )


@login_required
def following(request):
    """ Gets posts from users which the current user if following """

    following = request.user.user_set.all()
    posts = process_posts(
        Post.objects.filter(author__in=following).order_by("-created"), request
    )

    return render(
        request,
        "network/index.html",
        {"page_obj": posts, "selected": "following", "form": PostForm},
    )


@login_required
def posts(request):
    """ Creates a post via POST method """

    if request.method == "POST" and "add_post" in request.POST:
        post = PostForm(request.POST)
        post = post.save(commit=False)
        post.author = request.user
        post.save()
    return HttpResponseRedirect(reverse("index"))


def user(request, user_id):
    """ Gets user profile and user's posts, followers count, and following count """
    user = get_object_or_404(User, id=user_id)
    following = request.user in user.followers.all()
    is_you = request.user == user
    following_count = user.user_set.count()
    followers_count = user.followers.count()
    posts = process_posts(
        Post.objects.filter(author=user).order_by("-created"), request
    )
    return render(
        request,
        "network/index.html",
        {
            "profile": user,
            "page_obj": posts,
            "is_following": following,
            "is_you": is_you,
            "following": following_count,
            "followers": followers_count,
        },
    )


@login_required
def posts_edit(request, post_id):
    """ PUT update for a post """

    post = get_object_or_404(Post, id=post_id)
    if request.method == "PUT" and post.author == request.user:
        data = json.loads(request.body)
        post.content = data.get("content")
        post.save()
        return HttpResponse()
    return HttpResponseForbidden()


@login_required
def can_edit_post(request, post_id):
    """ Checks if user can edit post """

    can_edit = False
    post = get_object_or_404(Post, id=post_id)
    can_edit = request.user == post.author
    return JsonResponse({"canEdit": can_edit})


@login_required
def follow(request, user_id):
    """ Follows / unfollows user """

    user = get_object_or_404(User, id=user_id)
    if request.method == "PUT" and user != request.user:
        if request.user in user.followers.all():
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)
        return HttpResponse()
    return HttpResponseForbidden()


@login_required
def followers_count(request, user_id):
    """ Gets user account followers count """
    user = get_object_or_404(User, id=user_id)
    if request.method == "GET":
        return JsonResponse({"followers": user.followers.count()})
    return HttpResponseForbidden()


@login_required
def like(request, post_id):
    """ PUT Likes / unlikes post
        GET gets post like count and if current user liked the post """

    if request.method == "PUT":
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        post.save()
        return HttpResponse()
    elif request.method == "GET":
        post = get_object_or_404(Post, id=post_id)
        like_count = {
            "count": post.likes.count(),
            "liked": request.user in post.likes.all(),
        }
        return JsonResponse(like_count)
    return HttpResponseForbidden()


def login_view(request):
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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
