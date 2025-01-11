from django.urls import path
from . import views


urlpatterns = [
    path('ajax/add-to-cart', views.ajax_add_to_cart, name='ajax_add_to_cart'),

    path('cart/', views.cartPage, name='cart'),

    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),

    path('add-item/', views.add_item, name='add_item'),

    path('add-restaurant/', views.add_restaurant, name='add_restaurant'),

    path('wishlist/', views.wishlist, name='wishlist'),

    path('ajax/add-to-wishlist/', views.ajax_add_to_wishlist, name='ajax_add_to_wishlist'),

    path('checkout/', views.checkout, name='checkout'),

    path('calculate-distance/<int:item_id>/', views.calculate_distance_view, name='calculate_distance'),
]