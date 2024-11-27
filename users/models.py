from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    verification_code = models.UUIDField(default=uuid.uuid4, editable=False)
    is_seller = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) # Track when the profile was created

    def __str__(self):
        return f"{self.user.username}'s Profile"
