from django.db import models
from django.conf import settings


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    image = models.ImageField(upload_to='menu_images/')
    date_added = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"
    
    def get_total_price(self):
        return self.quantity * self.item.price