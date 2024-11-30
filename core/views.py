from django.shortcuts import render
from orders.models import Item, CartItem, WishListItem, Restaurant
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from django.http import JsonResponse

def homePage(request):
    query = request.GET.get('q', '')
    restaurant_filter = request.GET.get('restaurant', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    items = Item.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )


    if restaurant_filter:
        items = items.filter(restaurant__name=restaurant_filter)
    
    if min_price:
        items = items.filter(price__gte=min_price)
    
    if max_price:
        items = items.filter(price__lte=max_price)
    
    paginator = Paginator(items, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    restaurants = Restaurant.objects.all()

    user_wishlist = set()        
    total_items = 0
    if request.user.is_authenticated:
        user_wishlist = set(
            WishListItem.objects.filter(user=request.user).values_list('item_id', flat=True)
        )
        total_items = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    context = {
        'items': items,
        'total_items': total_items, 
        'user_wishlist': user_wishlist or None,
        'query': query,
        'restaurants': restaurants,
        'restaurant_filter': restaurant_filter,
        'min_price': min_price,
        'max_price': max_price,
        'page_obj': page_obj,
        }
    return render(request, 'core/index.html', context)

def autocomplete(request):
    query = request.GET.get('q', '')
    if query:
        item_matches = Item.objects.filter(name__icontains=query).values_list('name', flat=True)
        suggestions = list(item_matches)
        return JsonResponse({'suggestions': suggestions})
    return JsonResponse({'suggestions': []})

def contactPage(request):
    return render(request, 'core/contact.html')
