from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    fullname = forms.CharField(max_length=150, required=True, label='Full Name', widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300'}))

    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300'}))

    address = forms.CharField(max_length=200, required=False, label='Address', widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300'}), label='Password', help_text='Your password must be at least 8 character long.')

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300'}), label='Password Confirmation', help_text='Your password must be at least 8 character long.')

    class Meta:
        model = User
        fields = ['fullname', 'email', 'address', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                fullname = self.cleaned_data['fullname'],
                phone_number = self.cleaned_data.get('phone_number'),
                address = self.cleaned_data.get('address'),
            )
        return user


class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300'}))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'phone_number', 'address', 'is_seller']
        labels = {
            'fullname': 'Full Name',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'is_seller': 'Apply to be a seller',
        }
        help_texts = {
            'is_seller': 'Check this box if you would like to register a seller on the platform.'
        }
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'profile-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'profile-input'}),
            'address': forms.TextInput(attrs={'class': 'profile-input'}),
            'is_seller': forms.CheckboxInput(attrs={'class': 'form-check-input'},)
        }
