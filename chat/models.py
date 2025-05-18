from email.policy import default

from django.db import models
from app.models import CustomUser
# Create your models here.
class Chat(models.Model):
    members = models.ManyToManyField(CustomUser, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    is_group = models.BooleanField(default=False)

    def __str__(self):
        return f"Chat {self.id} - Members: {', '.join([p.email for p in self.participants.all()])}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE,null=True, related_name="messages")
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True, related_name="sent_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}: {self.content}"