from django.contrib import admin

from .models import User,Category,Listing,comment,Bid
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(comment)
admin.site.register(Bid)