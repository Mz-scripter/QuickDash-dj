from django.shortcuts import render
from orders.models import Item

def homePage(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'core/index.html', context)

def contactPage(request):
    return render(request, 'core/contact.html')
