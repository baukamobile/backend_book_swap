from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import *
from rest_framework import permissions, viewsets
from .serializers import *

def view_mes(request):
    return HttpResponse("Hello, world. You're at the polls view.")

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
