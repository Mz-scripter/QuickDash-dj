from django.shortcuts import render
from orders.models import Item, CartItem
from django.db.models import Sum

def homePage(request):
    items = Item.objects.all()
    total_items = 0
    if request.user.is_authenticated:
        total_items = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    context = {'items': items, 'total_items': total_items}
    return render(request, 'core/index.html', context)

def contactPage(request):
    return render(request, 'core/contact.html')
