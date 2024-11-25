from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    fullname = forms.CharField(max_length=150, required=True, label='Full Name')
    email = forms.EmailField(required=True, label='Email')
    phone_number = forms.CharField(max_length=15, required=False, label='Phone Number (+234 xxx xxxx xxx)')
    address = forms.CharField(max_length=200, required=False, label='Address')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password', help_text='Your password must be at least 8 character long.')

    class Meta:
        model = User
        fields = ['fullname', 'email', 'phone_number', 'address', 'password1']
    
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
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
