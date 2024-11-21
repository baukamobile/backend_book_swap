from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Custom user manager to manage User creation
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)  # Ensure password is hashed
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Superuser should be active

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)

# Custom User model
class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.email})"

# Book model representing a book
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional if the book is for exchange
    condition_choices = [('new', 'New'), ('used', 'Used')]
    condition = models.CharField(max_length=10, choices=condition_choices)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)  # Optional image for the book
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

# Transaction model for book sales between users
class Transaction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold_books")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bought_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status_choices = [('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

    def __str__(self):
        return f"Transaction {self.id} - {self.book.title} from {self.seller.email} to {self.buyer.email}"

# Exchange model for book swaps between users
class Exchange(models.Model):
    offeror = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offered_books")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_books")
    offeror_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="offered_in_exchange")
    receiver_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="received_in_exchange")
    status_choices = [('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exchange {self.id}: {self.offeror.email} offers {self.offeror_book.title} for {self.receiver.email}'s {self.receiver_book.title}"

# Wishlist model to store books a user wants
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s wishlist for {self.book.title}"

