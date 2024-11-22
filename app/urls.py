from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet,
                    BookViewSet,
                    TransactionViewSet,
                    ExchangeViewSet,
                    WishlistViewSet,
                    RegisterView,
                    LoginView,
                    LogoutView,
                    # LogoutView = RegisterView.as_view())
                    )
# Create a router and register your viewsets
router = DefaultRouter()
router.register(    r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'exchanges', ExchangeViewSet)
router.register(r'wishlist', WishlistViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


#bauka some@gmail.com qwerty