from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryN = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryN
    
class Bid(models.Model):
    bid= models.FloatField(default=0)
    user=  models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="userBid")
    
    
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=900)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, null=True, blank=True, related_name="bidPrice")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingwatchlist")
    def __str__(self):
        return self.title

class comment(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="creatercomment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name="listingcomment")
    message = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.message} comment on {self.listing}"



    