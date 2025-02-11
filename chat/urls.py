from django.urls import path
from chat.views import MessageListAPIView
urlpatterns = [
    path('messages/',MessageListAPIView.as_view()),
]