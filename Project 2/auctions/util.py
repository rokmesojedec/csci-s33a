""" Helper functions for auctions app """
from decimal import Decimal
from .models import Comment, CommentForm, BidForm


def set_listing_current_bid(listings):
    """This utility function iterates through listings list and determines
        current bid value by looking through related entries in bids table
        or using own initial_bid value """
    for listing in listings:
        if len(listing.bid_listing.all()) > 0:
            listing.current_bid = listing.bid_listing.all().order_by("-amount")[0].amount
        else:
            listing.current_bid = listing.initial_bid
    return listings


def create_listing_context(request, listing):
    """ Creates context object for viewlisting template """
    comments = Comment.objects.filter(item=listing)

    # Determine if the item is on watchlist by current user
    is_watchlisted = request.user.is_authenticated and len(request.user.watchlist_user.filter(id=listing.id)) > 0

    # Determine if current user is the creator of the listing
    is_owner = request.user.is_authenticated and listing.author == request.user

    # Determine the current_bid value by checking if listing has any
    # related bid entries, if so, take the highest value
    # if no bids were added, then use the inital bid value
    bids = listing.bid_listing.all()
    bid_count = len(bids)

    if bid_count > 0:
        current_bid = bids.order_by("-amount")[0].amount
        highest_bid_owner = bids.order_by("-amount")[0].bidder == request.user
    else:
        current_bid = listing.initial_bid
        highest_bid_owner = False

    # Ternary operator source: https://book.pythontips.com/en/latest/ternary_operators.html
    context = {
        "listing": listing,
        "comment_form": CommentForm,
        "comments": comments,
        "bid_form": BidForm,
        "watchlist_value": ("Add to Watchlist", "Remove from Watchlist")[is_watchlisted],
        "is_watchlisted": is_watchlisted,
        "current_bid": current_bid,
        "is_owner": is_owner,
        "bid_count": bid_count,
        "highest_bid_owner": highest_bid_owner,
        "category": listing.category,
        "bids": bids
    }

    # Set the minimum value attribute for bid amount to either listing's initial bid
    # or highest bid. If there are existing bids, then the next bid value has to be
    # bigger by at least 0.01, if not use initial bid value

    min_value = (context["current_bid"],
                 context["current_bid"] + Decimal(0.01))[context["current_bid"] is not listing.initial_bid]
    BidForm.helper.layout[0].attrs['min'] = min_value

    # Round the value to remove the float conversion imprecision
    BidForm.helper.layout[0].attrs['value'] = round(min_value, 2)

    # Prepare context dict. Used to pass data to template
    return context
