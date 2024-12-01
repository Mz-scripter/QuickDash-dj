from .models import Coupon, CartItem
import requests
from geopy.distance import geodesic

HERE_API_KEY = 'js1J-ZC70g74K0RzzJPUsaTB-lu3Cq4kDvqXwVaJnmc'
GEOCODING_URL = "https://geocode.search.hereapi.com/v1/geocode"

def validate_and_apply_coupon(code, total_amount):
    """
    Validates and applies a coupon.
    Args:
        code (str): Coupon code
        total_amount (Decimal): Total cart amount
    Returns:
        tuple: (discounted_amount, error_message)
    """
    try:
        coupon = Coupon.objects.get(code=code)
        if not coupon.is_valid():
            return total_amount, "Coupon is invalid or expired."
        
        if coupon.discount_type == "fixed":
            discounted_amount = max(total_amount - coupon.discount_value, 0)
        elif coupon.discount_type == "percent":
            discounted_amount = max(total_amount * (1 - coupon.discount_value / 100), 0)
        else:
            return total_amount, "Invalid discount type."
        
        coupon.times_used += 1
        coupon.save()
        return discounted_amount, None
    except Coupon.DoesNotExist:
        return total_amount, "Coupon does not exist."

def get_user_cart(user):
    """
    Retrieves the user's cart as a queryset of CartItems.
    """
    return CartItem.objects.filter(user=user)

def calculate_cart_total(user):
    """
    Calculates the total price of all items in the user's cart.
    """
    cart_items = get_user_cart(user)
    return sum(item.get_total_price() for item in cart_items)

def get_coordinates_here(address):
    """Get latitude and longitude of an address using the HERE Geocoding API."""
    params = {
        "q": address,
        "apiKey": HERE_API_KEY,
    }
    response = requests.get(GEOCODING_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            coordinates = data['items'][0]['position']
            return coordinates['lat'], coordinates['lng']
    return None

def calculate_distance(coord1, coord2):
    """Calculate the distance between two coordinates using the geopy library."""
    return geodesic(coord1, coord2).kilometers