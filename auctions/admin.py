from django.contrib import admin

from .models import Bid, Listing, User, Comments, Categories


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "price", "created_at")


class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "starting_bid",
        "highest_bid_id",
        "image_url",
        "category",
        "is_active",
        "winner",
        "author",
        "created_at",
    )
    filter_horizontal = ("saved_by",)


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "password", "profile_pic")


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "user", "listing", "created_at")


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Bid, BidAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Categories, CategoriesAdmin)
