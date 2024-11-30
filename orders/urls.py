from django.urls import path
from . import views


urlpatterns = [
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cartPage, name='cart'),

    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),

    path('add-item/', views.add_item, name='add_item'),

    path('add-restaurant/', views.add_restaurant, name='add_restaurant'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/toggle/<int:item_id>/', views.toggle_wishlist, name='toggle_wishlist'),

    path('checkout/', views.checkout, name='checkout')
]