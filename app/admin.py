from django.contrib import admin

# Register your models here.
from .models import CustomUser,Exchange, Book,Transaction,Wishlist,RegionUser,Genres
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email','name','region_user','user_book_id')
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(RegionUser)

admin.site.register(Exchange)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','description','genre','price','region','owner')
admin.site.register(Book,BookAdmin)

admin.site.register(Transaction)

admin.site.register(Wishlist)
admin.site.register(Genres)



#bauka some@gmail.com qwerty
#admin any@gmail.com qwerty
#sat@gmail.com sat 4444