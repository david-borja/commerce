from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


# User
class User(AbstractUser):
    profile_pic = models.CharField(max_length=128, blank=True)

    @staticmethod
    def get_profile_pic_by_username(usernames):
        # Query the database for users with the given usernames
        users = User.objects.filter(username__in=usernames)
        # Create a dictionary to store profile pics
        profile_pics = {}
        # Iterate over the filtered users
        for user in users:
            # Add the username and profile pic URL to the dictionary
            profile_pics[user.username] = user.profile_pic

        return profile_pics


# Listing
class Listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    starting_bid = models.FloatField()
    highest_bid_id = models.ForeignKey(
        "Bid",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="lisitings_won",
    )  # string references ( "Bid" ) can be use for referencing models that are defined below
    image_url = models.CharField(max_length=128, blank=True)
    category = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    saved_by = models.ManyToManyField(
        User, blank=True, null=True, related_name="watchlist"
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="won_auctions",
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="published_listings"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Title: {self.title}, author: {self.author.username}"


# Bid
class Bid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing_bids"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.id}: {self.user} offered {self.price} for {self.listing}"


# Comments
class Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=128)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing_comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.id}: {self.user} commented "{self.text}" on {self.listing}'


# Categories
class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
