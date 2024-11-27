from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('verify/<uuid:code>/', views.verifyEmail, name='verify'),
    path('verify-email/', views.verifyEmailPage, name='verify-email'),

    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/<int:user_id>/<str:token>', views.password_reset_confirm, name='password_reset_confirm'),

    path('profile/', views.profilePage, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile')
]