from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chat.models import Message
from chat.serializers import MessageSerializer



class MessageListAPIView(APIView):
    def get(self,request):
        mes = Message.objects.all()
        serializer = MessageSerializer(mes,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
