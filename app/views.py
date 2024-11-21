from django.shortcuts import render
from django.http import HttpResponse
from .models import UserProfile, Book
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from .serializers import UserProfileSerializer, BooksSerializer
from rest_framework.exceptions import ValidationError  # Import for raising validation errors


# This is for handling the view that you mentioned (though it's not essential to the UserProfile logic)
def view_mes(request):
    return HttpResponse("Hello, world. You're at the polls view.")


# Update your UserProfileViewSet to handle the profile existence logic
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Create the user if it doesn't exist
        username = serializer.validated_data.get('user').get('username')
        email = serializer.validated_data.get('user').get('email')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Create a new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=serializer.validated_data.get('user').get('password')
            )

        # Save the UserProfile with the newly created user
        user_profile = serializer.save(user=user)

        # Return the profile data along with the user's ID
        return Response(UserProfileSerializer(user_profile).data, status=status.HTTP_201_CREATED)

# You can also add similar logic for other viewsets if needed
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [permissions.AllowAny]
