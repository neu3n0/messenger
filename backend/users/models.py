from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
        Custom user model
    """
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Age"
    )