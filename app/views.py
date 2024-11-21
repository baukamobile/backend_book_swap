from rest_framework import viewsets
from .models import CustomUser, Book, Transaction, Exchange, Wishlist
from .serializers import CustomUserSerializer, BookSerializer, TransactionSerializer, ExchangeSerializer, WishlistSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()  # Ensure queryset is defined
    serializer_class = CustomUserSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()  # Ensure queryset is defined
    serializer_class = BookSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()  # Ensure queryset is defined
    serializer_class = TransactionSerializer

class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()  # Ensure queryset is defined
    serializer_class = ExchangeSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()  # Ensure queryset is defined
    serializer_class = WishlistSerializer
