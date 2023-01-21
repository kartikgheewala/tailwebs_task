from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Create a user table.
    """
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, null=True)
    token = models.TextField(null=True)
    role = models.CharField(max_length=50, default="admin")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    class Meta:
        db_table = 'user'
