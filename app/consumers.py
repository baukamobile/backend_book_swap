import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Chat, Message, CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Add user to the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from the group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        sender_email = data.get("sender")
        recipient_email = data.get("recipient")

        # Get sender and recipient
        sender = await sync_to_async(CustomUser.objects.get)(email=sender_email)
        recipient = await sync_to_async(CustomUser.objects.get)(email=recipient_email)

        # Fetch or create a chat for the sender and recipient
        chat = await sync_to_async(self.get_or_create_chat)(sender, recipient)

        # Store the message in the database
        new_message = await sync_to_async(Message.objects.create)(
            chat=chat,
            sender=sender,
            recipient=recipient,
            content=message,
        )

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": new_message.content,
                "sender": sender.email,
                "recipient": recipient.email,
                "timestamp": str(new_message.timestamp),
            },
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    def get_or_create_chat(self, sender, recipient):
        # Ensure a chat exists between the sender and recipient
        chat, created = Chat.objects.get_or_create()
        chat.members.add(sender, recipient)
        return chat
