from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing


def index(request):
    listings = (
        Listing.objects.all()
    )  # it returns a queryset containing all the objects (instances) of the Listing model

    # here it should also check if a user is logged in.
    # in that case, exclude listings published by them

    return render(request, "auctions/index.html", {"listings": listings})


def detail(request, listing_id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        # Instance of the Listing model -> dot notation
        is_saved_by_user = request.user.watchlist.filter(pk=listing_id).exists()
        listing.is_saved_by_user = is_saved_by_user
        return render(request, "auctions/detail.html", {"listing": listing})
    else:
        return render(request, "auctions/login.html")


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

            return render(request, "auctions/index.html")
        else:
            return render(request, "auctions/create.html")
    else:
        return render(request, "auctions/login.html")
