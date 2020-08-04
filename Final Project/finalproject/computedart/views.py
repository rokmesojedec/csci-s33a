import json
import base64
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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


def process_configs(configs):
    """ Helper for creating calculated values for each config, and appending related colors """
    for config in configs:
        config.colors = config.config_color.all()
        config.image_width = config.grid_width * config.square_size
        config.image_height = config.grid_height * config.square_size


def config(request):
    """ Returns all config objects """
    configs = Configuration.objects.order_by("-created")
    process_configs(configs)
    return render(
        request,
        "computedart/index.html",
        {"selected": "configurations", "configs": configs},
    )


def showcase(request):
    """ Returns config objects with saved images used for showcasing """
    return render(
        request,
        "computedart/showcase.html",
        {
            "selected": "showcase",
            "configs": Configuration.objects.order_by("-created").exclude(
                image_file=""
            ),
        },
    )


@login_required
def user_configs(request, user_id):
    """ Returns configs authored by specified user """
    user = get_object_or_404(User, id=user_id)
    configs = Configuration.objects.filter(author=user)
    process_configs(configs)
    context = {"configs": configs}
    context["selected"] = ("configurations", "myconfig")[user == request.user]
    return render(request, "computedart/index.html", context)


@login_required
def create_config(request):
    """ Creates config via POST """
    if request.method == "POST":
        config = Configuration()
        config.square_size = request.POST["square_size"]
        config.grid_width = request.POST["grid_width"]
        config.grid_height = request.POST["grid_height"]
        config.title = request.POST["title"]
        config.circle_chance = request.POST["circle_chance"]
        config.color_chance = request.POST["color_chance"]
        config.animate = (False, True)[request.POST.get("animate", False) == "on"]
        config.author = request.user
        config.save()
        for key in request.POST:
            if key.startswith("color-"):
                color = Color()
                color.configuration = config
                color.color = request.POST[key]
                color.save()
        return HttpResponseRedirect(reverse("config", args=(config.id,)))
    return render(
        request,
        "computedart/createconfig.html",
        {"selected": "createconfig", "form": ConfigurationForm},
    )

@login_required
def upload(request, config_id):
    """ Uploads an images to an exisiting config object via PUT"""
    # Uploading image must be done via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    config = get_object_or_404(Configuration, id=config_id)

    if config.author != request.user:
        return HttpResponseForbidden()

    data = json.loads(request.body)
    image = data.get("image")
    format, imgstr = image.split(";base64,")
    ext = format.split("/")[-1]
    image_file = ContentFile(base64.b64decode(imgstr), name=config.title + "." + ext)
    config.image_file = image_file
    config.save()

    return HttpResponse(status=204)


def view_config(request, config_id):
    """ returns view where an individual config is rendered in a canvas """
    config = get_object_or_404(Configuration, id=config_id)
    return render(
        request,
        "computedart/viewconfig.html",
        {
            "selected": "createconfig", 
            "config_id": config.id,
            "is_author": config.author == request.user,
            "is_saved" : config.image_file != ""
        },
    )


def get_config(request, config_id):
    """ returns config JSON """
    config = get_object_or_404(Configuration, id=config_id)

    json = {
        "id": config.id,
        "title": config.title,
        "size": config.square_size,
        "width": config.grid_width,
        "height": config.grid_height,
        "animate": config.animate,
        "circleChance": config.circle_chance,
        "colorChance": config.color_chance
    }

    colors = []

    if len(config.config_color.all()) > 0:
        for color in config.config_color.all():
            colors.append('"' + color.color + '"')

    json["colors"] = "[" + ", ".join(colors) + "]"

    return JsonResponse(json)


def login_view(request):
    """ logs in user """
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("showcase"))
        else:
            return render(
                request,
                "computedart/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "computedart/login.html")


def logout_view(request):
    """ logs out user """
    logout(request)
    return HttpResponseRedirect(reverse("showcase"))


def register(request):
    """ registers user """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "computedart/register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "computedart/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("showcase"))
    else:
        return render(request, "computedart/register.html")
