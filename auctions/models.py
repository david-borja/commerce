from django.contrib.auth.models import AbstractUser
from django.db import models

# User
class User(AbstractUser):
    pass

# Listing
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    starting_bid = models.FloatField()
    price = models.FloatField()
    image = models.CharField(max_length=128)
    category = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    saved_by = models.ManyToManyField(User, blank=True, related_name="watchlist")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_auctions")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="published_listings")
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.id}: {self.title}, last price {self.price}"

# Bids
class Bids(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.id}: {self.user} offered {self.price} for {self.listing}"

# Comments
class Comments(models.Model):
    text = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return f"{self.id}: {self.user} commented \"{self.text}\" on {self.listing}"

# Categories
class Categories(models.Model):
    name = models.CharField(max_length=64)