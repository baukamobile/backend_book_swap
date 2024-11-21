from django.contrib import admin

# Register your models here.
from .models import CustomUser,Exchange, Book,Transaction,Wishlist

admin.site.register(CustomUser)

admin.site.register(Exchange)

admin.site.register(Book)

admin.site.register(Transaction)

admin.site.register(Wishlist)



