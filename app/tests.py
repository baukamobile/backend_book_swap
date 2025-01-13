from django.test import TestCase
from app.models import CustomUser,Book
from backendflutter.settings import namedb


class CustomUser(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(name="testpy1",email="testpy1@gmail.com",password="testpy1")
        CustomUser.objects.create_user(name="testpy2", email="testpy2@gmail.com", password="testpy2")
    def test_user_name(self):
        testpy1 = CustomUser.objects.get(name="testpy1")
        testpy2 = CustomUser.objects.get(name="testpy2")
        self.assertEqual(testpy1)
        self.assertEqual(testpy1)