from django.contrib import admin

# Register your models here.
from .models import User,Exchange, Book,Transaction,Wishlist

admin.site.register(User)

admin.site.register(Exchange)

admin.site.register(Book)

admin.site.register(Transaction)

admin.site.register(Wishlist)



