from .models import CartItem
from django.db.models import Sum


def cart_item_count(request):
    total_items = 0
    if request.user.is_authenticated:
        total_items = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    return {'total_items': total_items}