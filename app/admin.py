from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserProfile)
admin.site.register(Exchange)
admin.site.register(Book)
admin.site.register(Transaction)
admin.site.register(Wishlist)