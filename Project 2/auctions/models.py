""" Models used in auctions app """
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm

# Using Crispy forms to generate bootstrap forms
# https://django-crispy-forms.readthedocs.io/en/latest/index.html

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from crispy_forms.bootstrap import PrependedText

# Default date time column to now
# Source: https://stackoverflow.com/questions/2771676/django-datetime-issues-default-datetime-now


class Category(models.Model):
    """ Category model """
    title = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"{self.title}"


class User(AbstractUser):
    """ User model """
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    """ Listing model """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_author", editable=False)
    title = models.CharField(max_length=256)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True)
    initial_bid = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    image_URL = models.URLField(blank=True)
    category = models.ForeignKey(
        Category, blank=True, null=True, related_name="category_items", on_delete=models.SET_NULL)
    watchlist = models.ManyToManyField(
        User, blank=True, related_name="watchlist_user")
    bids = models.ManyToManyField(User, through="Bid", blank=True, related_name="bids")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"


class ListingForm(ModelForm):
    """ Listing model form """
    class Meta:
        """ Listing form meta class """
        model = Listing
        fields = ["title", "description", "initial_bid", "image_URL", "category"]
    helper = FormHelper()
    helper.form_class = "form-group"
    helper.layout = Layout(
        Field("title", css_class="form-control mt-2 mb-3"),
        Field("description", rows="3", css_class="form-control mb-3"),
        PrependedText("initial_bid", "€", css_class="mb-3"),
        Field("image_URL", css_class="form-control mb-3"),
        Field("category", css_class="form-control mb-3"),
        Submit("add_listing", "Create Listing")
    )


class Bid(models.Model):
    """ Bid model """
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bid_author")
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bid_listing")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.item} | {self.bidder} (€{self.amount})"


class BidForm(ModelForm):
    """ Bid form model """
    class Meta:
        """ Bid form meta class """
        model = Bid
        fields = ["amount"]
    helper = FormHelper()
    helper.form_class = "form-group"
    helper.form_show_labels = False
    helper.layout = Layout(
        PrependedText("amount", "€", css_class="mb-3 mt-3"),
        Submit("place_bid", "Bid",)
    )


class Comment(models.Model):
    """ Comment model """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_author")
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comment_listing")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True)


class CommentForm(ModelForm):
    """ Comment form model """
    class Meta:
        """ Comment form meta class """
        model = Comment
        fields = ["content"]
    helper = FormHelper()
    helper.form_show_labels = False
    helper.form_class = "form-group"
    helper.layout = Layout(
        Field("content", rows="3", css_class="form-control mb-3"),
        Submit("post_comment", "Post Comment")
    )
