from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import User
from django.views.decorators.csrf import csrf_protect
from .models import Profile
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model




token_generator = PasswordResetTokenGenerator()



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
            messages.error(request, 'Email does not exist. Please register.')
            return redirect('register')
        
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or Password incorrect')

    context = {'page': page}
    return render(request, 'users/login.html', context)

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

            profile = Profile.objects.create(
                user=user,
                fullname=form.cleaned_data.get('fullname'),
                address=form.cleaned_data.get('address'),
                phone_number=form.cleaned_data.get('phone_number'),
            )

            verification_code = profile.verification_code

            verification_url = request.build_absolute_uri(reverse('verify', args=[verification_code]))

            send_mail(
                'Verify Your Email Address',
                f'Click the link below to verify your email address: \n\n {verification_url}',
                'mzscripterx5@gmail.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Verification email sent! Please check your inbox.')
            return redirect('register')
        else:
            # Check for duplicate email error
            if 'email' in form.errors.as_data():
                for error in form.errors['email']:
                    if 'already registered' in error:
                        messages.info(request, 'An account with this email already exists. Please login.')
                        return redirect('login')
            messages.error(request, 'Error occured during registration.')
    return render(request, 'users/register.html', context)

def verifyEmail(request, code):  
    try:
        profile = get_object_or_404(Profile, verification_code=code)
        if profile.is_verified == True:
            messages.info(request, 'Your email is already verified.')
            return redirect('login')
        else:
            profile.is_verified = True
            profile.save()
            return redirect('verify-email')
    except Exception as e:
        messages.error(request, 'Invalid verification link.')
        return redirect('register')
   
def verifyEmailPage(request):
    return render(request, 'users/verify.html')

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = token_generator.make_token(user)
                reset_url = request.build_absolute_uri(
                    reverse('password_reset_confirm', args=[user.pk, token])
                )

                # Send email
                send_mail(
                    'Reset Your Password',
                    f'Click the link to reset your password: {reset_url}',
                    'mzscripterx5@gmail.com',  # Replace with your sender email
                    [email],
                )
                messages.success(request, 'Password reset link has been sent to your email.')
                return redirect('password_reset_request')
            except User.DoesNotExist as e:
                messages.error(request, f'Email address not found. Error: {str(e)}')
                return redirect('password_reset_request')
        else:
            messages.error(request, 'Invalid email format.')
    else:
        form = PasswordResetForm()
    return render(request, 'users/auth-process.html', {'page': 'reset-request', 'form': PasswordResetForm})


def password_reset_confirm(request, user_id, token):
    page = 'reset-token'
    context = {'page': page}
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        if not token_generator.check_token(user, token):
            messages.error(request, 'Invalid or expired token.')
            return redirect('password_reset_request')
        
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'users/auth-process.html', context)
    except User.DoesNotExist():
        messages.error(request, 'Invalid user.')
        return redirect('password_reset_request')

@login_required(login_url='/login')
def profilePage(request):
    profile = get_object_or_404(Profile, user=request.user)
    context = {
        'fullname': profile.fullname,
        'email': request.user.email,
        'phone_number': profile.phone_number,
        'address': profile.address,
        'is_seller': profile.is_seller,
        'allowed_emails': ['mzscripterx5@gmail.com', 'adekomuheez567@gmail.com']
    }
    return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def update_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updates successfully.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'users/update-profile.html', {'form': form})