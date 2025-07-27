from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='Calculatorapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('calculator/', views.CalculadoraView.as_view(), name='calculator'),
    path('limpar-historico/', views.limpar_historico, name='limpar_historico'),
    path('confirm-email/<uuid:token>/', views.confirm_email_view, name='confirm_email'),
    path('resend-confirmation/', views.resend_confirmation_view, name='resend_confirmation'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password_confirm_view, name='reset_password_confirm'),
]