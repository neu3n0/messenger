from django.db import models
from users.models import User


class TestApp(models.Model):
    """
    TestApp
    """

    arg1 = models.CharField(max_length=100, verbose_name="arg1")
    arg2 = models.FloatField(verbose_name="arg2")

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tests", verbose_name="Owner"
    )
