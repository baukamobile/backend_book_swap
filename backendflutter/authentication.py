# authentication.py
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find the user by email
            user = User.objects.get(email=username)  # Here 'username' will be the email
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
