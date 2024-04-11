from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid


def index(request):
    if request.user.is_authenticated:
        listings = Listing.objects.exclude(author=request.user)
    else:
        listings = (
            Listing.objects.all()
        )  # it returns a queryset containing all the objects (instances) of the Listing model

    return render(request, "auctions/index.html", {"listings": listings})


def detail(request, listing_id):
    is_authenticated = request.user.is_authenticated
    # Instance of the Listing model -> dot notation
    listing = Listing.objects.get(pk=listing_id)
    # user_watchlist = request.user.watchlist.all()  # .all() very important!
    if is_authenticated:
        is_saved_by_user = request.user.watchlist.filter(pk=listing_id).exists()
        if request.method == "POST" and request.POST.get("_method") == "PATCH":
            submitted_bid = float(request.POST.get("bid"))
            if submitted_bid:
                highest_bid = listing.highest_bid.price if listing.highest_bid else listing.starting_bid
                is_new_highest = submitted_bid > highest_bid
                if is_new_highest:
                    bid = Bid.objects.create(
                        listing=listing,
                        user=request.user,
                        price=submitted_bid,
                    )
                    listing.highest_bid = bid
                    listing.save()
            if is_saved_by_user:
                listing.saved_by.remove(request.user)
                is_saved_by_user = False
            else:
                listing.saved_by.add(request.user)
                is_saved_by_user = True
        listing.is_saved_by_user = is_saved_by_user
    listing.current_highest = listing.highest_bid.price if listing.highest_bid else listing.starting_bid
    params = { "listing": listing, "is_authenticated": is_authenticated }
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
