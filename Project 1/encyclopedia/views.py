from . import util
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.views.decorators.csrf import csrf_exempt
import random
import markdown2


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    content = forms.CharField(widget=forms.Textarea, label="Content", required=True)


# Adding placeholder attribute to Django Form
# https://stackoverflow.com/questions/44133562/django-add-placeholder-text-to-form-field/44133785
class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia', 'class': 'search'}))


# search_form paramter has to be in all contexts passed to request because it is needed
# by layout.html which is inherited in all pages used in this app
context = {
    "search_form": SearchForm()
    }


def index(request):
    list_entries = util.list_entries()
    results = None
    # check if "q" get parameter is present
    q = request.GET.get("q", None)
    # if q exists this means the user submitted a search query
    if q is not None:
        # if query fully matches any entry while ignoring the case
        # we redirect directly to that entry
        if q.upper() in (entry.upper() for entry in list_entries):
            # return entry(request, q)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(q,)))
        else:
            # check for partial query match
            # source: https://kite.com/python/answers/how-to-check-if-a-list-contains-a-substring-in-python
            results = [entry for entry in list_entries if q.upper() in entry.upper()]
    else:
        results = list_entries

    context["q"] = q
    context["entries"] = results
    return render(request, "encyclopedia/index.html", context)


def entry(request, entry_title):
    entry = util.get_entry(entry_title)
    context["title"] = entry_title
    if entry is not None:
        context["entry"] = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", context)
    else:
        context["error_type"] = "404"
        return render(request, "encyclopedia/error.html", context)


def random_entry(request):
    # reverse with args
    # source: https://docs.djangoproject.com/en/3.0/ref/urlresolvers/
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=(random.choice(util.list_entries()),)))


@csrf_exempt
def add(request):
    context["crud_type"] = "add"
    context["title"] = "New Entry"
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            # If the entry with submitted title exists, redirect to error page
            entry_title = form.cleaned_data["title"]
            if util.get_entry(entry_title) is not None:
                context["error_type"] = "duplicate"
                context["title"] = entry_title
                return render(request, "encyclopedia/error.html", context)
            # otherwise save the entry and redirect to main page
            util.save_entry(entry_title, form.cleaned_data["content"])
            # reverse with args
            # source: https://docs.djangoproject.com/en/3.0/ref/urlresolvers/
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(entry_title,)))
        else:
            context["form"] = form
            return render(request, "encyclopedia/crud.html", context)
    else:
        # no POST submission, just show empty form
        context["form"] = NewEntryForm()
        return render(request, "encyclopedia/crud.html", context)


@csrf_exempt
def edit(request, entry_title):
    entry = util.get_entry(entry_title)
    context["title"] = entry_title

    # if entry isn't found, show error 404
    if entry is None:
        context["error_type"] = "404"
        return render(request, "encyclopedia/error.html", context)
    else:
        context["crud_type"] = "edit"

    # Form is create on request, as it needs to be prepopulated with entry content
    class EditEntryForm(forms.Form):
        content = forms.CharField(
            widget=forms.Textarea, label="Content", required=True, initial=entry)

    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            util.save_entry(entry_title, form.cleaned_data["content"])
            # reverse with args
            # source: https://docs.djangoproject.com/en/3.0/ref/urlresolvers/
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(entry_title,)))
        else:
            context['form'] = form
            return render(request, "encyclopedia/crud.html", context)
    else:
        context["form"] = EditEntryForm()
        return render(request, "encyclopedia/crud.html", context)
