from django import forms
from .models import Item, Restaurant


class ItemForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300'})
    )
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300', 'rows': 4})
    )
    rating = forms.DecimalField(
        max_digits=3,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300', 'min': 0, 'max': 5, 'step': 0.1})
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300'})
    )
    restaurant = forms.ModelChoiceField(
        queryset=Restaurant.objects.all(),
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300'})
    )
    class Meta:
        model = Item
        fields = ['name', 'price', 'restaurant', 'description', 'rating', 'image']


class RestaurantForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300'})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300'})
    )
    class Meta:
        model = Restaurant
        fields = ['name', 'address']