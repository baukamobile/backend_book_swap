from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, CustomUser, Genres
from decimal import Decimal


class BookAPITest(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Создаем жанр
        self.genre = Genres.objects.create(name="Fiction")

        # Авторизуемся
        self.client.login(username="testuser", password="testpassword")

    def test_create_book(self):
        # Тестируем создание книги через API
        url = "/api/books/"  # Адрес твоего API для books
        data = {
            "title": "Test Book",
            "author": "Test Author",
            "description": "Test Description",
            "genre": self.genre.id,
            "price": "12.99",
            "condition": "new",
            "owner": self.user.id,
        }

        # Отправляем POST-запрос
        response = self.client.post(url, data, format="json")

        # Проверяем, что ответ имеет статус 201 (успешное создание)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что книга была создана в базе данных
        book = Book.objects.get(title="Test Book")
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.price, Decimal("12.99"))
        self.assertEqual(book.condition, "new")

    def test_get_books(self):
        # Создаем книгу для тестирования GET-запроса
        book = Book.objects.create(
            title="Another Test Book",
            author="Test Author",
            description="Test Description",
            genre=self.genre,
            price=Decimal("15.99"),
            condition="used",
            owner=self.user,
        )

        # Тестируем GET-запрос
        url = "/api/books/"
        response = self.client.get(url)

        # Проверяем, что ответ успешный
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что созданная книга присутствует в списке
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Another Test Book")

    def test_book_detail(self):
        # Создаем книгу для тестирования детализированного представления
        book = Book.objects.create(
            title="Another Test Book",
            author="Test Author",
            description="Test Description",
            genre=self.genre,
            price=Decimal("15.99"),
            condition="used",
            owner=self.user,
        )

        # Тестируем GET-запрос на получение детализированной информации о книге
        url = f"/api/books/{book.id}/"
        response = self.client.get(url)

        # Проверяем, что ответ успешный
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что данные книги в ответе совпадают
        self.assertEqual(response.data["title"], "Another Test Book")
        self.assertEqual(response.data["author"], "Test Author")
        self.assertEqual(response.data["price"], "15.99")
        self.assertEqual(response.data["condition"], "used")
