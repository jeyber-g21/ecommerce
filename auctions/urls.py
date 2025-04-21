from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createlisting, name="create"),
    path("categories", views.categories, name="categories"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("remove_watchlist/<int:id>", views.remove, name="removewatchlist"),
    path("add_watchlist/<int:id>", views.add, name="addwatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("New_comment/<int:id>", views.addcomment, name="newcomment"),
    path("Add_bid/<int:id>", views.newbid, name="newbid"),
    path("Close_auction/<int:id>", views.closeauction, name="closeauction")
    ]
