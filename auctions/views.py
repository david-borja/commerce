from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing
from .utils import process_bid, toggle_bookmark, close_listing, get_current_highest, get_footer


def index(request):
    # it returns a queryset containing all the objects (instances) of the Listing model
    listings = Listing.objects.filter(is_active=True)

    for listing in listings:
        listing.current_highest = get_current_highest(listing)
        listing.footer = get_footer(listing)
    return render(request, "auctions/index.html", {"listings": listings, "title": "Active Listings"})

def watchlist(request):
    is_authenticated = request.user.is_authenticated
    if is_authenticated:
        user_watchlist = request.user.watchlist.all()  # .all() very important!
        for listing in user_watchlist:
            listing.current_highest = get_current_highest(listing)
            listing.footer = get_footer(listing)
        return render(request, "auctions/index.html", {"listings": user_watchlist, "title": "Watchlist"})
    else:
        return HttpResponseRedirect(reverse("login"))

def won_auctions(request):
    is_authenticated = request.user.is_authenticated
    if is_authenticated:
        won_auctions = request.user.won_auctions.all()
        for listing in won_auctions:
            listing.current_highest = get_current_highest(listing)
            listing.footer = get_footer(listing)
        return render(request, "auctions/index.html", {"listings": won_auctions, "title": "Won Auctions"})
    else:
        return HttpResponseRedirect(reverse("login"))

def published_listings(request):
    is_authenticated = request.user.is_authenticated
    if is_authenticated:
        published_listings = request.user.published_listings.all()
        for listing in published_listings:
            listing.current_highest = get_current_highest(listing)
            listing.footer = get_footer(listing, "published")
        return render(request, "auctions/index.html", {"listings": published_listings, "title": "Published Listings"})
    else:
        return HttpResponseRedirect(reverse("login"))

def detail(request, listing_id):
    is_authenticated = request.user.is_authenticated
    # Instance of the Listing model -> dot notation
    listing = Listing.objects.get(pk=listing_id)
    # user_watchlist = request.user.watchlist.all()  # .all() very important!
    error = None
    if is_authenticated:
        is_saved_by_user = request.user.watchlist.filter(pk=listing_id).exists()
        listing.is_saved_by_user = is_saved_by_user
        if request.method == "POST" and request.POST.get("_method") == "PATCH":
            toggle_key = request.POST.get("toggle_key")
            submitted_bid = request.POST.get("bid")
            if toggle_key:
                listing.is_active = close_listing(listing) if toggle_key == "is_active" else listing.is_active
                listing.is_saved_by_user = toggle_bookmark(is_saved_by_user, listing, request.user) if toggle_key == "is_saved" else is_saved_by_user
                return HttpResponseRedirect(reverse("detail", args=[listing_id]))
            if submitted_bid:
                error = process_bid(submitted_bid, listing, request)
                if not error:
                    return HttpResponseRedirect(reverse("detail", args=[listing_id]))
    params = { "listing": listing, "is_authenticated": is_authenticated, "message": error }
    return render(request, "auctions/detail.html", params)


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
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


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
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST["title"]
            description = request.POST["description"]
            starting_bid = request.POST["starting_bid"]
            author = request.user
            listing = Listing(
                title=title,
                description=description,
                starting_bid=starting_bid,
                author=author,
            )
            listing.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html")
    else:
        return HttpResponseRedirect(reverse("login"))
