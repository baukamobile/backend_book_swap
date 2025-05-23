from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from . views import *

# Create a router and register your viewsets
router = DefaultRouter()
router.register(    r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'exchanges', ExchangeViewSet)
router.register(r'wishlist', WishlistViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', register.as_view()),
    path('api/login/', loginView.as_view()),
    path('api/user/', userget.as_view()),
    path('api/logout/',logoutView.as_view()),
    path('api/regions/', RegionsView.as_view()),
    path('api/genres/', GenresView.as_view()),
    path('api/users/<int:user_id>/books/', user_books, name='user-books'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#bauka some@gmail.com qwerty


# {
#   "username": "testuse1r",
#   "email": "testuser122@example.com",
#   "password": "password123",
#   "name": "Test User221"
# } title,author,description(max 40 word),price
