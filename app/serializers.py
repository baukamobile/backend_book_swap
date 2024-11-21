from rest_framework import serializers
from .models import CustomUser, Book, Transaction, Exchange, Wishlist

# Serializer for CustomUser model
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login']

# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)  # Read-only field showing the owner of the book

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'price', 'condition', 'image', 'owner', 'created_at', 'updated_at']

# Serializer for Transaction model
class TransactionSerializer(serializers.ModelSerializer):
    seller = CustomUserSerializer(read_only=True)  # Read-only field showing the seller
    buyer = CustomUserSerializer(read_only=True)  # Read-only field showing the buyer
    book = BookSerializer(read_only=True)  # Read-only field showing the book in the transaction

    class Meta:
        model = Transaction
        fields = ['id', 'seller', 'buyer', 'book', 'price', 'date', 'status']

# Serializer for Exchange model
class ExchangeSerializer(serializers.ModelSerializer):
    offeror = CustomUserSerializer(read_only=True)  # Read-only field showing the offeror
    receiver = CustomUserSerializer(read_only=True)  # Read-only field showing the receiver
    offeror_book = BookSerializer(read_only=True)  # Read-only field showing the book offered by the offeror
    receiver_book = BookSerializer(read_only=True)  # Read-only field showing the book received by the receiver

    class Meta:
        model = Exchange
        fields = ['id', 'offeror', 'receiver', 'offeror_book', 'receiver_book', 'status', 'date']

# Serializer for Wishlist model
class WishlistSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # Read-only field showing the user
    book = BookSerializer(read_only=True)  # Read-only field showing the book on the wishlist

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'book', 'added_at']
