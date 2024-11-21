from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    restaurant = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    image = models.ImageField(upload_to='menu_images/')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
