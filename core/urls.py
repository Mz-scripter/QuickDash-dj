from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.homePage, name='home'),
    path('contact/', views.contactPage, name='contact')
]