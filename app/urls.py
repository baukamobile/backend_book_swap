from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'profile', UserProfileViewSet)
router.register(r'books', BookViewSet)
urlpatterns = [
    path('func/', view_mes),
    path('api-auth/', include('rest_framework.urls')),
    # path('books', include('rest_framework.urls')),
]