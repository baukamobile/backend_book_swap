from .models import *
from rest_framework import serializers


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'
# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # Include user.id as user_id

    class Meta:
        model = UserProfile
        fields = ['user', 'user_id', 'address', 'phone_number', 'created_at', 'date_of_birth']  # Add date_of_birth here


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

