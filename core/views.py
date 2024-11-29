from django.shortcuts import render
from orders.models import Item, CartItem, WishListItem
from django.db.models import Sum, Q

def homePage(request):
    query = request.GET.get('q', '')
    items = Item.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )
    user_wishlist = set()        
    total_items = 0
    if request.user.is_authenticated:
        user_wishlist = set(
            WishListItem.objects.filter(user=request.user).values_list('item_id', flat=True)
        )
        total_items = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    context = {'items': items, 'total_items': total_items, 'user_wishlist': user_wishlist or None}
    return render(request, 'core/index.html', context)

def contactPage(request):
    return render(request, 'core/contact.html')
