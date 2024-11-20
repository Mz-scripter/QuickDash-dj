from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('verify-email/', views.verifyEmailPage, name='verify-email'),
    path('reset-request/', views.resetRequestPage, name='reset-request'),
    path('reset-token/', views.resetTokenPage, name='reset-token'),

    path('profile/', views.profilePage, name='profile'),
    path('edit-profile', views.editProfilePage, name='edit-profile'),
]