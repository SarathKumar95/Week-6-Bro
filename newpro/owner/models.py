from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

