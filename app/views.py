from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from .serializers import UserProfileSerializer, BooksSerializer
from rest_framework.exceptions import ValidationError  # Import for raising validation errors
from rest_framework import viewsets
from .models import User, Book, Transaction, Exchange, Wishlist
from .serializers import UserSerializer, BookSerializer, TransactionSerializer, ExchangeSerializer, WishlistSerializer

# ViewSet for User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ViewSet for Book
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# ViewSet for Transaction
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

# ViewSet for Exchange
class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer

# ViewSet for Wishlist
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer


#7765674523