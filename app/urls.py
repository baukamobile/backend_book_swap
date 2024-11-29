from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    UserViewSet,
    BookViewSet,
    TransactionViewSet,
    ExchangeViewSet,
    WishlistViewSet,
    get_users,
    CustomTokenRefreshView,
    logout,
    register,
)
from rest_framework_simplejwt.views import TokenObtainPairView  # Importing this view

# Create a router and register your viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'exchanges', ExchangeViewSet)
router.register(r'wishlist', WishlistViewSet)

urlpatterns = [
    # API viewsets
    path('api/', include(router.urls)),

    # JWT Authentication
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Corrected this line
    path('api/logout/', logout, name='logout'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    # User Registration (Make this part of API)
    path('api/register/', register, name='register'),

    # Get Users (ensure authentication)
    path('api/users/', get_users, name='get_users'),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#bauka some@gmail.com qwerty


# {
#   "username": "testuse1r",
#   "email": "testuser122@example.com",
#   "password": "password123",
#   "name": "Test User221"
# } title,author,description(max 40 word),price


#
# Hamlet
# Author: William Shakespeare
# Description: A tragedy about Prince Hamlet seeking revenge against his uncle, who has murdered his father and married his mother.
# Price: $9.99
# Crime and Punishment
# Author: Fyodor Dostoevsky
# Description: A psychological novel about a young man’s moral dilemmas after committing a crime in St. Petersburg.
# Price: $12.99
# Pride and Prejudice
# Author: Jane Austen
# Description: A romantic novel about the evolving love story between Elizabeth Bennet and Mr. Darcy in 19th-century England.
# Price: $8.99
# The Alchemist
# Author: Paulo Coelho
# Description: A young shepherd embarks on a journey to find treasure, learning about destiny and self-discovery.
# Price: $14.99
# To Kill a Mockingbird
# Author: Harper Lee
# Description: A young girl learns about racism, injustice, and morality as her father defends a black man falsely accused of rape.
# Price: $10.99
# The Adventures of Tom Sawyer
# Author: Mark Twain
# Description: A young boy navigates life in the fictional town of St. Petersburg, creating mischief and learning life lessons.
# Price: $7.99
# War and Peace
# Author: Leo Tolstoy
# Description: A sweeping historical novel set during the Napoleonic Wars, exploring Russian society and personal struggles.
# Price: $15.99