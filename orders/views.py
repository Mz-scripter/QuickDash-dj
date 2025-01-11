from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item, CartItem, WishListItem
from django.contrib import messages
from .forms import ItemForm, RestaurantForm
from users.models import Profile
from django.http import HttpResponseForbidden, JsonResponse
from .utils import validate_and_apply_coupon, get_user_cart, calculate_cart_total, get_coordinates_here, calculate_distance
import json
from datetime import timedelta
from django.db.models import Sum


@login_required(login_url='login')
def ajax_add_to_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, id=item_id)

        # Get or create the cart item
        cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        # Get updated cart total
        total_items = sum(item.quantity for item in CartItem.objects.filter(user=request.user))

        return JsonResponse({'status': 'success', 'total_items': total_items})
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'})

@login_required(login_url='login')
def cartPage(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    total_items = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    context = {'cart_items': cart_items, 'total_price': total_price, 'total_items': total_items}
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
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, "Item added successfully!")
            return redirect('profile')
        else:
            messages.error(request, f"Error adding item. Please check the form. {form.errors}")
    else:
        form = ItemForm()
    return render(request, 'orders/add-item.html', {'form': form})

@login_required(login_url='login')
def add_restaurant(request):
    allowed_emails = ['mzscripterx5@gmail.com', 'adekomuheez567@gmail.com']
    if request.user.email not in allowed_emails:
        return HttpResponseForbidden("You don't have access this page.")
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

@login_required(login_url='login')
def toggle_wishlist(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    wishlist_item, created = WishListItem.objects.get_or_create(user=request.user, item=item)

    if created:
        messages.success(request, f"{item.name} added to your wish list!")
    else:
        wishlist_item.delete()
        messages.info(request, f"{item.name} removed from your wish list.")
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required(login_url='login')
def wishlist(request):
    wishlist_items = WishListItem.objects.filter(user=request.user).select_related('item')
    return render(request, 'orders/wishlist.html', {'wishlist_items': wishlist_items})

@login_required(login_url='login')
def ajax_add_to_wishlist(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, id=item_id)

        # Check if the item is already in the wishlist
        wishlist_item, created = WishListItem.objects.get_or_create(user=request.user, item=item)

        if not created:
            wishlist_item.delete()
            status = 'removed'
        else:
            wishlist_item.save()
            status = 'added'
        
        return JsonResponse({'status': status})
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'})

@login_required(login_url='login')
def checkout(request):
    cart_items = get_user_cart(request.user)
    total_amount = calculate_cart_total(request.user)
    discounted_amount = total_amount
    coupon_discount = 0
    error_message = None

    if request.method == 'POST':
        coupon_code = request.POST.get("coupon")
        if coupon_code:
            discounted_amount, error_message = validate_and_apply_coupon(coupon_code, total_amount)
            coupon_discount = total_amount - discounted_amount
    
    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "total_amount": total_amount,
        "discounted_amount": round(discounted_amount, 2),
        "coupon_discount": round(coupon_discount, 2),
        "error_message": error_message,
    })

def calculate_distance_view(request, item_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_lat = data.get('latitude')
        user_lon = data.get('longitude')

        # Fallback to the user's registered address if location access is denied
        if not user_lat or not user_lon:
            profile = get_object_or_404(Profile, user=request.user)
            user_address = profile.address
            user_coords = get_coordinates_here(user_address)
        else:
            user_coords = (user_lat, user_lon)
        item = get_object_or_404(Item, id=item_id)
        restaurant = item.restaurant
        restaurant_coords = (restaurant.latitude, restaurant.longitude)

        # Calculate distance
        distance = calculate_distance(user_coords, restaurant_coords)

        # Estimated time
        average_speed_kmh = 50
        time_hours = distance / average_speed_kmh
        time_minutes = time_hours * 60
        estimated_time = str(timedelta(minutes=round(time_minutes)))
        return JsonResponse({'distance': round(distance, 2), 'time': estimated_time})