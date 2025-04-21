from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing, comment, Bid


update=3

def listing(request,id):
    listingdata=Listing.objects.get(pk=id)
    listwatchlist = request.user in listingdata.watchlist.all()
    comments=comment.objects.filter(listing=listingdata)
    trueowner=request.user.username==listingdata.owner.username
    return render(request, "auctions/listing.html",{
        "Listing":listingdata, 
        "listwatchlist":listwatchlist,
        "comments":comments, "trueowner":trueowner
    })

def closeauction(request, id):
    listingdata=Listing.objects.get(pk=id)
    listingdata.isActive=False
    listingdata.save()
    trueowner=request.user.username==listingdata.owner.username
    listwatchlist = request.user in listingdata.watchlist.all()
    comments=comment.objects.filter(listing=listingdata)
    return render(request, "auctions/listing.html",{
        "Listing":listingdata, "message":"Auction is closed",
        "update": 1, "listwatchlist":listwatchlist,
        "comments":comments, "trueowner":trueowner
    })

def newbid(request,id):
    newbid=request.POST["newbid"]
    listingdata=Listing.objects.get(pk=id)
    listwatchlist = request.user in listingdata.watchlist.all()
    comments=comment.objects.filter(listing=listingdata)
    trueowner=request.user.username==listingdata.owner.username
    if int(newbid)>listingdata.price.bid:
        actualbid=Bid(user=request.user,bid=int(newbid))
        actualbid.save()
        listingdata.price=actualbid
        listingdata.save()
        return render(request,"auctions/listing.html",{
            "Listing":listingdata, "message":"bid was added",
            "update": 1, "listwatchlist":listwatchlist,
            "comments":comments, "trueowner":trueowner,
        })
    if int(newbid)<listingdata.price.bid:
        return render(request,"auctions/listing.html",{
            "Listing":listingdata, "message":"Error: bid is lower, it was not added",
            "update": 2, "listwatchlist":listwatchlist,
            "comments":comments, "trueowner":trueowner
        })
    

def addcomment (request, id):
    currentuser=request.user
    listingdata=Listing.objects.get(pk=id)
    message=request.POST['newcomment']
    newcomment=comment(
        creater=currentuser,listing=listingdata,message=message
    )
    newcomment.save()
    return HttpResponseRedirect(reverse("listing",args=(id, )))
    

def remove(request,id):
    listingdata=Listing.objects.get(pk=id)
    currentuser=request.user
    listingdata.watchlist.remove(currentuser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def add(request,id):
    listingdata=Listing.objects.get(pk=id)
    currentuser=request.user
    listingdata.watchlist.add(currentuser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))
  
    
def watchlist(request):
    currentuser=request.user
    listing=Listing.objects.filter(watchlist=currentuser)
    return render(request, "auctions/watchlist.html",{
        "Listings": listing
    })
    

def index(request):
    active=Listing.objects.filter(isActive=True)
    categories= Category.objects.all()
    return render(request, "auctions/index.html",{
        "Listings": active,"categories":categories
    })



def categories(request):
    if request.method=="POST":
        categoryindex=request.POST['category']
        category=Category.objects.get(categoryN=categoryindex)
        active=Listing.objects.filter(isActive=True, category=category)
        categories= Category.objects.all()
        return render(request, "auctions/index.html",{
        "Listings": active,"categories":categories
    })
    return

def createlisting(request):
    if request.method=="GET":
        categories= Category.objects.all()
        users=User.objects.all()
        return render (request, "auctions/createL.html",{
            "categories":categories, "users":users
        })
    else:
        title=request.POST["title"]
        description=request.POST["description"]
        image=request.POST["image"]
        price=request.POST["price"]
        category=request.POST["category"]
        currentUser= request.user
        categoryinf= Category.objects.get(categoryN=category)
        bid=Bid(bid=float(price), user=currentUser)
        bid.save()

        ListingN= Listing(
            title=title,description=description,image=image,
            price=bid,owner=currentUser,category=categoryinf

        )
        ListingN.save()
        return HttpResponseRedirect(reverse("index"))

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


