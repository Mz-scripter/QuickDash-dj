from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item, CartItem
from django.contrib import messages
from .forms import ItemForm, RestaurantForm
from users.models import Profile
from django.http import HttpResponseForbidden



@login_required(login_url='login')
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('home')

@login_required(login_url='login')
def cartPage(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    context = {'cart_items': cart_items, 'total_price': total_price,}
    return render(request, 'orders/cart.html', context)

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def increase_quantity(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required(login_url='login')
def decrease_quantity(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')

login_required(login_url='login')
def add_item(request):
    profile = get_object_or_404(Profile, user=request.user)
    if not profile.is_seller:
        return HttpResponseForbidden("You must be a seller to access this page.")
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Item added successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Error adding item. Please check the form.")
    else:
        form = ItemForm()
    return render(request, 'orders/add-item.html', {'form': form})

@login_required(login_url='login')
def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            return redirect('profile')
    else:
        form = RestaurantForm()
    return render(request, 'orders/add-restaurant.html', {'form': form})