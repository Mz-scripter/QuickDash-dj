from django.db import models
from django.conf import settings
from django.utils import timezone
from cloudinary.models import CloudinaryField



class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        from .utils import get_coordinates_here
        if not self.latitude or not self.longitude:
            coords = get_coordinates_here(self.address)
            if coords:
                self.latitude, self.longitude = coords
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    image = CloudinaryField('images', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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


class WishListItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s favorite: {self.item.name}"


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(
        max_length=10, choices=[("fixed", "Fixed"), ("percent", "Percent")]
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateTimeField()
    usage_limit = models.IntegerField(default=1)
    times_used = models.IntegerField(default=0)

    def is_valid(self):
        """Checks if the coupon is valid."""
        return (
            self.times_used < self.usage_limit and self.expiration_date > timezone.now()
        )
    
    def __str__(self):
        return f"Coupon {self.code} - {self.discount_type} {self.discount_value}"