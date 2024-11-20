from django.shortcuts import render

def loginPage(request):
    page = 'login'
    context = {'page': page}
    return render(request, 'users/login-register.html', context)

def registerPage(request):
    page = 'register'
    context = {'page': page}
    return render(request, 'users/login-register.html', context)

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
