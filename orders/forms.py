from django import forms
from .models import Item, Restaurant


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'restaurant', 'description', 'rating', 'image', 'restaurant']
        widget = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'restaurant': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 5, 'step': 0.1,}),
            # 'image': forms.FileInput(attrs={'class': 'form-control'}),
            'restaurant': forms.Select(attrs={'class': 'form-control'})
        }


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'})
        }