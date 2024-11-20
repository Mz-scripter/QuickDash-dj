from django.shortcuts import render

from django.shortcuts import render

def homePage(request):
    return render(request, 'core/index.html')

def contactPage(request):
    return render(request, 'core/contact.html')
