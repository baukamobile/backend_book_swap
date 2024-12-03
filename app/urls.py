from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
# from .views import (UserViewSet,
#                     BookViewSet,
#                     TransactionViewSet,
#                     ExchangeViewSet,
#                     WishlistViewSet,
#                      get_users,
# register,
#                     )

from . views import *

# from .views import CustomTokenObtainPairView, CustomTokenRefreshView, logout, register
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
    path('api/logout/',logoutView.as_view())


    # path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/logout/', logout),
    # path('api/register/', register),
    # path('api/users/', get_users),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#bauka some@gmail.com qwerty


# {
#   "username": "testuse1r",
#   "email": "testuser122@example.com",
#   "password": "password123",
#   "name": "Test User221"
# } title,author,description(max 40 word),price
