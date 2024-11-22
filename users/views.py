from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from .models import Profile


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
    
        try:
            user = User.objects.get(email=email)
        
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('login')
        
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or Password incorrect')

    context = {'page': page}
    return render(request, 'users/login-register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@csrf_protect
def registerPage(request):
    page = 'register'
    form = CustomUserCreationForm()
    context = {'page': page, 'form': form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.save()

            Profile.objects.create(
                user=user,
                fullname=form.cleaned_data.get('fullname'),
                address=form.cleaned_data.get('address'),
                phone_number=form.cleaned_data.get('phone_number'),
            )

            login(request, user)
            return redirect('home')
        else: 
            print('Error')
    return render(request, 'users/register.html', context)

def verifyEmailPage(request):
    page = 'verify-email'
    
    context = {'page': page}
    return render(request, 'users/auth-process.html', context)

def resetRequestPage(request):
    page = 'reset-request'
    context = {'page': page}
    return render(request, 'users/auth-process.html', context)

def resetTokenPage(request):
    page = 'reset-token'
    context = {'page': page}
    return render(request, 'users/auth-process.html', context)

def profilePage(request):
    return render(request, 'users/profile.html')

def editProfilePage(request):
    return render(request, 'users/edit-profile.html')
