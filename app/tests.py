from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import Book, Genres, Transaction, Exchange, Wishlist
CustomUser = get_user_model()
class CustomUserTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="password123"
        )
    def test_create_user(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("password123"))

    def test_user_str(self):
        self.assertEqual(str(self.user), "Test User (test@example.com)")
class BookTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(name="Owner", email="owner@example.com", password="password")
        self.genre = Genres.objects.create(genre="fiction")
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            description="Book Description",
            genre=self.genre,
            condition="new",
            owner=self.user
        )

    def test_create_book(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.owner.email, "owner@example.com")

    def test_book_str(self):
        self.assertEqual(str(self.book), "Test Book by Author")


class TransactionTest(TestCase):
    def setUp(self):
        self.seller = CustomUser.objects.create_user(name="Seller", email="seller@example.com", password="password")
        self.buyer = CustomUser.objects.create_user(name="Buyer", email="buyer@example.com", password="password")
        self.book = Book.objects.create(title="Sell Book", author="Author", description="Desc", condition="used",
                                        owner=self.seller)
        self.transaction = Transaction.objects.create(
            seller=self.seller,
            buyer=self.buyer,
            book=self.book,
            price=50.00,
            status="pending"
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.book.title, "Sell Book")
        self.assertEqual(self.transaction.status, "pending")

    def test_transaction_str(self):
        self.assertIn("Transaction", str(self.transaction))


class ExchangeTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(name="User1", email="user1@example.com", password="password")
        self.user2 = CustomUser.objects.create_user(name="User2", email="user2@example.com", password="password")
        self.book1 = Book.objects.create(title="Book1", author="Author1", description="Desc1", condition="new",
                                         owner=self.user1)
        self.book2 = Book.objects.create(title="Book2", author="Author2", description="Desc2", condition="used",
                                         owner=self.user2)
        self.exchange = Exchange.objects.create(
            offeror=self.user1,
            receiver=self.user2,
            offeror_book=self.book1,
            receiver_book=self.book2,
            status="pending"
        )

    def test_exchange_creation(self):
        self.assertEqual(self.exchange.status, "pending")

    def test_exchange_str(self):
        self.assertIn("Exchange", str(self.exchange))


class WishlistTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(name="WishlistUser", email="wishlist@example.com",
                                                   password="password")
        self.book = Book.objects.create(title="Wishlist Book", author="Author", description="Desc", condition="new",
                                        owner=self.user)
        self.wishlist = Wishlist.objects.create(user=self.user, book=self.book)

    def test_wishlist_creation(self):
        self.assertEqual(self.wishlist.user.email, "wishlist@example.com")
        self.assertEqual(self.wishlist.book.title, "Wishlist Book")

    def test_wishlist_str(self):
        self.assertIn("wishlist", str(self.wishlist))
