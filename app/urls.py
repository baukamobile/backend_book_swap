from django.urls import path,include
from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'profile', views.UserProfileViewSet)
# router.register(r'books', views.BookViewSet)
# # router.register(r'account', UserProfileViewSet)
#
# urlpatterns = [
#     path('func/', views.view_mes),
#     path('api-auth/', include('rest_framework.urls')),
#     # path('books', include('rest_framework.urls')),
# ]

router = routers.DefaultRouter()
router.register(r'profile', views.UserProfileViewSet)
router.register(r'books', views.BookViewSet)

urlpatterns = [
    path('func/', views.view_mes),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),  # Include the router's URLs
]