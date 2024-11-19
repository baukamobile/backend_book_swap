from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user

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


class Transaction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold_books")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bought_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status_choices = [('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

    def __str__(self):
        return f"Transaction {self.id} - {self.book.title} from {self.seller.username} to {self.buyer.username}"


class Exchange(models.Model):
    offeror = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offered_books")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_books")
    offeror_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="offered_in_exchange")
    receiver_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="received_in_exchange")
    status_choices = [('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exchange {self.id}: {self.offeror.username} offers {self.offeror_book.title} for {self.receiver.username}'s {self.receiver_book.title}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist for {self.book.title}"
