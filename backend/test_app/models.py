from django.db import models

class TestApp(models.Model):
    """
        TestApp
    """

    arg1 = models.CharField(max_length=100, verbose_name="arg1")
    arg2 = models.FloatField(verbose_name="arg2")