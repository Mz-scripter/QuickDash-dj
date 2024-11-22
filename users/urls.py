from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('verify/<uuid:code>/', views.verifyEmail, name='verify'),
    path('verify-email/', views.verifyEmailPage, name='verify-email'),

    path('reset-request/', views.resetRequestPage, name='reset-request'),
    path('reset-token/', views.resetTokenPage, name='reset-token'),

    path('profile/', views.profilePage, name='profile'),
    path('edit-profile', views.editProfilePage, name='edit-profile'),
]