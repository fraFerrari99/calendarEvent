from django.contrib.auth.models import AbstractUser #you need to customize it
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    #abstract user start from scratch
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.email