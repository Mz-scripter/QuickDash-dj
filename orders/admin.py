from django.contrib import admin
from .models import Item, Coupon, Restaurant

admin.site.register(Item)
admin.site.register(Restaurant)
admin.site.register(Coupon)
