from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
class RegionUser(models.Model):
    CITY_CHOICES = [
        ('almaty', 'Almaty'),
        ('astana', 'Astana'),
        ('shymkent', 'Shymkent'),
        ('aktobe', 'Aktobe'),
        ('karaganda', 'Karaganda'),
    ]
    city = models.CharField(max_length=100,choices=CITY_CHOICES, null=True)
    def __str__(self):
        return self.city
# Custom User model
class CustomUser(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    region_user = models.ForeignKey(RegionUser, on_delete=models.SET_NULL, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_img/', null=True, blank=True, default='profile_img/avtr.jpg')  # Profile image
    book_image = models.ImageField(upload_to='book_img/', null=True, blank=True)  # Profile image

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
    image = models.ImageField(upload_to='book_img/', blank=True, null=True)  # Optional image for the book
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

# Transaction model for book sales between users
class Transaction(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sold_books")
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bought_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status_choices = [('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

    def __str__(self):
        return f"Transaction {self.id} - {self.book.title} from {self.seller.email} to {self.buyer.email}"

# Exchange model for book swaps between users
class Exchange(models.Model):
    offeror = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="offered_books")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_books")
    offeror_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="offered_in_exchange")
    receiver_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="received_in_exchange")
    status_choices = [('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exchange {self.id}: {self.offeror.email} offers {self.offeror_book.title} for {self.receiver.email}'s {self.receiver_book.title}"

# Wishlist model to store books a user wants
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s wishlist for {self.book.title}"

class Chat(models.Model):
    members = models.ManyToManyField(CustomUser, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id} - Members: {', '.join([p.email for p in self.participants.all()])}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)



#
# Name	Email	Password
# John Smith	john.smith@example.com	Jsm!89L@o#12
# Alice Johnson	alice.j@example.com	AJo@2023p#45
# Robert Brown	robert.brown@example.com	RBr$7Kx!90%T
# Emily Davis	emily.davis@example.com	EmD@84!cX$2W
# Michael Wilson	michael.w@example.com	MWil*123#q@9


