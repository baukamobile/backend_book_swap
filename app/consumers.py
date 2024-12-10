from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  # Подключение

    async def disconnect(self, close_code):
        pass  # Отключение

    async def receive(self, text_data):
        # Обрабатываем входящие сообщения
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Пример декодирования сообщения
        # Если сообщение поступило в Unicode формате
        print(f"Получено сообщение: {message}")

        # Отправляем сообщение обратно клиенту
        await self.send(text_data=json.dumps({
            'message': message
        }))
