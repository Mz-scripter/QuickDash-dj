from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
