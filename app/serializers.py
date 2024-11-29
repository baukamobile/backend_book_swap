from rest_framework import serializers
from .models import CustomUser, Book, Transaction, Exchange, Wishlist
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

UserModel = get_user_model()

# Serializer for CustomUser model
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'password', 'address', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}  # Make password write-only for security

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

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

# Serializer for User Registration (CustomUser)
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password', 'address']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

# Serializer for User Login (CustomUser)
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate the user using email and password
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        attrs['user'] = user
        return attrs

# JWT Serializer for Token (RefreshToken)
class JWTSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    class Meta:
        fields = ['refresh', 'access']

    def create(self, validated_data):
        refresh = RefreshToken.for_user(validated_data['user'])
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

