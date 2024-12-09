import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/chat/"  # Замените на ваш URL
    async with websockets.connect(uri) as websocket:
        # Отправка сообщения
        await websocket.send(json.dumps({'message': 'Привет от клиента!'}))

        # Получение сообщения
        response = await websocket.recv()
        data = json.loads(response)
        print('Message from server:', data['message'])

# Запуск асинхронной функции
asyncio.get_event_loop().run_until_complete(test_websocket())
