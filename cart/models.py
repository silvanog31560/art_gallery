from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product
User = get_user_model()

class UserItem(models.Model):
        items = models.ForeignKey(Product, on_delete=models.CASCADE)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField(default=1)
        added = models.DateTimeField(auto_now=True)
        invoice = models.CharField(max_length=20, blank=True)
        sold = models.DateTimeField(blank=True, null=True)
        tracking_number = models.CharField(max_length=25, blank=True)

        @property
        def total_price(self):
            total_price = (self.quantity * self.items.price)/100
            return "{0:.2f}".format(total_price)

        @property
        def stripe_price(self):
            return self.quantity * self.items.price

        def __str__(self):
            return self.items.title +" quantity: "+ str(self.quantity)
