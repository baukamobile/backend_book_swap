from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, BookViewSet, TransactionViewSet, ExchangeViewSet, WishlistViewSet

# Create the router and register viewsets with explicit basenames
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')  # Specify basename
router.register(r'books', BookViewSet, basename='book')  # Specify basename
router.register(r'transactions', TransactionViewSet, basename='transaction')  # Specify basename
router.register(r'exchanges', ExchangeViewSet, basename='exchange')  # Specify basename
router.register(r'wishlists', WishlistViewSet, basename='wishlist')  # Specify basename

urlpatterns = [
    path('api/', include(router.urls)),
]
