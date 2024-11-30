from .models import Coupon, CartItem

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