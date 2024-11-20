from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cartPage, name='cart'),
]