import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract JWT token from the WebSocket headers
        token = None
        headers = dict(self.scope.get('headers', []))  # Convert list of headers to dictionary

        # Find the Authorization header
        authorization = headers.get(b'authorization', None)
        if authorization:
            # Remove "Bearer " prefix if it exists
            token = authorization.decode().split(' ')[1] if authorization.startswith(b'Bearer ') else authorization.decode()

        if token:
            try:
                # Validate the token
                UntypedToken(token)  # This will raise an exception if the token is invalid
                self.user = await self.get_user_from_token(token)
            except (InvalidToken, TokenError):
                # If token is invalid, deny connection
                await self.close()
                return
        else:
            # If no token is provided, deny connection
            await self.close()
            return

        # Now, we proceed to the rest of the connection logic if the user is authenticated
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def get_user_from_token(self, token):
        """Helper function to get the user associated with a JWT token."""
        try:
            # Decode the token to get user information
            decoded_token = UntypedToken(token).payload
            user_id = decoded_token.get('user_id')  # Ensure the token includes 'user_id'

            # Fetch the user from the database
            user = await database_sync_to_async(get_user_model().objects.get)(id=user_id)
            return user
        except Exception as e:
            raise InvalidToken(f"Invalid token: {e}")
