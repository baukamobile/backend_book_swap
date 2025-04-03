from django.test import TestCase
from django.utils import timezone
from chat.models import Chat, Message
from app.models import CustomUser
from datetime import timedelta


class ChatModelTest(TestCase):

    def setUp(self):
        # Создание пользователей для чата
        self.user1 = CustomUser.objects.create_user(
            name="User1", email="user1@example.com", password="testpassword"
        )
        self.user2 = CustomUser.objects.create_user(
            name="User2", email="user2@example.com", password="testpassword"
        )
        # Создание чата с двумя участниками
        self.chat = Chat.objects.create()
        self.chat.members.set([self.user1, self.user2])
        self.chat.save()

    def test_chat_creation(self):
        # Проверка, что чат создан
        self.assertEqual(Chat.objects.count(), 1)
        chat = Chat.objects.first()
        self.assertEqual(chat.members.count(), 2)

    def test_chat_str_method(self):
        # Проверка, что __str__ правильно отображает информацию
        chat_str = str(self.chat)
        self.assertIn("Chat", chat_str)
        self.assertIn(self.user1.email, chat_str)
        self.assertIn(self.user2.email, chat_str)


class MessageModelTest(TestCase):

    def setUp(self):
        # Создание пользователей для сообщений
        self.user1 = CustomUser.objects.create_user(
            name="User1", email="user1@example.com", password="testpassword"
        )
        self.user2 = CustomUser.objects.create_user(
            name="User2", email="user2@example.com", password="testpassword"
        )
        # Создание чата
        self.chat = Chat.objects.create()
        self.chat.members.set([self.user1, self.user2])
        self.chat.save()

    def test_message_creation(self):
        # Отправка сообщения
        message = Message.objects.create(
            chat=self.chat,
            sender=self.user1,
            content="Hello, User2!",
        )
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.content, "Hello, User2!")
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.chat, self.chat)

    def test_message_str_method(self):
        # Проверка __str__ метода для сообщения
        message = Message.objects.create(
            chat=self.chat,
            sender=self.user1,
            content="Hello, User2!",
        )
        message_str = str(message)
        self.assertIn(str(self.user1), message_str)
        self.assertIn(message.content, message_str)

    def test_message_timestamp(self):
        # Проверка, что timestamp работает правильно
        message = Message.objects.create(
            chat=self.chat,
            sender=self.user1,
            content="Test message",
        )
        self.assertTrue(message.timestamp <= timezone.now())

    def test_message_is_read(self):
        # Проверка состояния is_read по умолчанию
        message = Message.objects.create(
            chat=self.chat,
            sender=self.user1,
            content="Unread message",
        )
        self.assertFalse(message.is_read)

