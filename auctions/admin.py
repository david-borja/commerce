from django import forms
from django.contrib import admin
from .models import Bid, Listing, User, Comments, Categories


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "price", "created_at")


class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "starting_bid",
        "highest_bid_id",
        "category",
        "is_active",
        "winner",
    )
    filter_horizontal = ("saved_by",)


class UserAdminForm(forms.ModelForm):
    watchlist = forms.ModelMultipleChoiceField(
        queryset=Listing.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple(
            verbose_name=("Watchlist"), is_stacked=False
        ),
    )

    class Meta:
        model = Listing
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(UserAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["watchlist"].initial = self.instance.watchlist.all()

    def save(self, commit=True):
        user = super(UserAdminForm, self).save(commit=False)

        if commit:
            user.save()

        if user.pk:
            user.watchlist.set(self.cleaned_data["watchlist"])

        return user


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ("username", "email")
    filter_horizontal = ("watchlist",)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "user", "listing", "created_at")


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Bid, BidAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Categories, CategoriesAdmin)
