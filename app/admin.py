from django.contrib import admin

# Register your models here.
from .models import CustomUser, Exchange, Book, Transaction, Wishlist, RegionUser, Genres, Message, Chat

admin.site.register(CustomUser)
admin.site.register(RegionUser)

admin.site.register(Exchange)

admin.site.register(Book)

admin.site.register(Transaction)

admin.site.register(Wishlist)
admin.site.register(Genres)

admin.site.register(Message)
admin.site.register(Chat)

