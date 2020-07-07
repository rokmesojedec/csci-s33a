from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

# default date time column to now
# source: https://stackoverflow.com/questions/2771676/django-datetime-issues-default-datetime-now


class Category(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_author", editable=False)
    title = models.CharField(max_length=256)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True)
    initial_bid = models.PositiveIntegerField(default=0)
    image_URL = models.URLField(blank=True)
    categories = models.ManyToManyField(
        Category, blank=True, related_name="category_items")
    wishlist = models.ManyToManyField(
        User, blank=True, related_name="wishlist_user")
    def __str__(self):
        return f"{self.title}"

# Create Form from model
# source: https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/
class ListingForm(ModelForm):
    class Meta: 
        model = Listing
        fields = ["title", "description", "initial_bid", "image_URL", "categories"]
        labels = {
            "intial_bid": _("Initial  Bid (€)"),
        }


class Bid(models.Model):
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bid_author")
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bid_listing")
    amount = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.item} | {self.bidder} (€{self.amount})"

class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_author")
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comment_listing")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True)
