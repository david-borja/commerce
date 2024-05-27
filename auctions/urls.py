from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("won-auctions", views.won_auctions, name="won_auctions"),
    path("published-listings", views.published_listings, name="published_listings"),
    path("listings/<str:listing_id>", views.detail, name="detail"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("comments", views.comments, name="comments"),
    path("__reload__/", include("django_browser_reload.urls")),
]
