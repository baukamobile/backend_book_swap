from django.urls import path
from .views import view_mes
urlpatterns = [
    path('', view_mes),
]