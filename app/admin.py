from django.contrib import admin

# Register your models here.
from .models import CustomUser,Exchange, Book,Transaction,Wishlist,RegionUser

admin.site.register(CustomUser)
admin.site.register(RegionUser)

admin.site.register(Exchange)

admin.site.register(Book)

admin.site.register(Transaction)

admin.site.register(Wishlist)



