from django.shortcuts import render
from django.http import HttpResponse
from .models import UserProfile, Book
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

    # Overriding perform_create to check if a UserProfile already exists
    def perform_create(self, serializer):
        user = serializer.validated_data.get('user')  # Get user from the validated data

        # Check if the user already has a UserProfile
        if UserProfile.objects.filter(user=user).exists():
            raise ValidationError("User profile with this user already exists.")

        # Save the profile if no existing profile
        serializer.save()


# You can also add similar logic for other viewsets if needed
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [permissions.AllowAny]
