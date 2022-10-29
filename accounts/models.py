from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True, unique=True)
    email = models.EmailField('Email Address', max_length=254, unique=True)

    def __str__(self):
        return self.username

class ShippingAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=25)
    zip_code = models.IntegerField()

    class Meta:
        verbose_name = "shipping address"
        verbose_name_plural = "shipping addresses"

    def __str__(self):
        return self.first_name
