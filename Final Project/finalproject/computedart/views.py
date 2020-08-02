from django.contrib.auth import authenticate, login, logout
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from .models import User, ConfigurationForm, Color, Configuration

# Create your views here.
def index(request):
    return render(request, "computedart/index.html")


def create_config(request):
    if request.method == "POST":
        config = Configuration()
        config.grid = request.POST["grid"]
        config.title = request.POST["title"]
        config.author = request.user
        config.save()
        for key in request.POST:
            if key.startswith("color-"):
                color = Color()
                color.configuration = config
                color.color = request.POST[key]
                color.save()
        return render(request, "computedart/index.html")
    return render(request, "computedart/createconfig.html",
    {
        "selected" : "createconfig",
        "form" : ConfigurationForm
    })

def view_config(request, config_id):
    config = get_object_or_404(Configuration, id=config_id)

    return render(request, "computedart/viewconfig.html",
    {
        "selected" : "createconfig",
        "config_id" : config.id
    })

def get_config(request, config_id):
    config = get_object_or_404(Configuration, id=config_id)

    json = {
        "id": config.id,
        "title": config.title,
        "grid": config.grid
        }

    colors = []

    if len(config.config_color.all()) > 0:
        for color in config.config_color.all():
            colors.append('"' + color.color + '"') 

    json["colors"] = "[" + ", ".join(colors) + "]"
    
    return JsonResponse(json)

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
                "computedart/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "computedart/login.html")


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
                request, "computedart/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "computedart/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "computedart/register.html")
