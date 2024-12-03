from rest_framework import serializers
from .models import User, Book, Transaction, Exchange, Wishlist
from django.contrib.auth import get_user_model, authenticate
UserModel = get_user_model()


from .models import User


#user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','second_name','email','age','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance

# Serializer for CustomUser model
# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'name', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login']
#         extra_kwargs = {'password': {'write_only': True}}  # Make password write-only for security
#
#     def create(self, validated_data):
#         # Ensure password is hashed when creating a new user
#         password = validated_data.pop('password', None)
#         user = super().create(validated_data)
#         if password:
#             user.set_password(password)
#             user.save()
#         return user
# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)  # Read-only field showing the owner of the book

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'price', 'condition', 'image', 'owner', 'created_at', 'updated_at']

# Serializer for Transaction model
class TransactionSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)  # Read-only field showing the seller
    buyer = UserSerializer(read_only=True)  # Read-only field showing the buyer
    book = BookSerializer(read_only=True)  # Read-only field showing the book in the transaction

    class Meta:
        model = Transaction
        fields = ['id', 'seller', 'buyer', 'book', 'price', 'date', 'status']

# Serializer for Exchange model
class ExchangeSerializer(serializers.ModelSerializer):
    offeror = UserSerializer(read_only=True)  # Read-only field showing the offeror
    receiver = UserSerializer(read_only=True)  # Read-only field showing the receiver
    offeror_book = BookSerializer(read_only=True)  # Read-only field showing the book offered by the offeror
    receiver_book = BookSerializer(read_only=True)  # Read-only field showing the book received by the receiver

    class Meta:
        model = Exchange
        fields = ['id', 'offeror', 'receiver', 'offeror_book', 'receiver_book', 'status', 'date']

# Serializer for Wishlist model
class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Read-only field showing the user
    book = BookSerializer(read_only=True)  # Read-only field showing the book on the wishlist

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'book', 'added_at']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


#New variant
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
