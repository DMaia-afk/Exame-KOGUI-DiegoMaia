from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import UserProfile, EmailConfirmationToken

class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="E-mail", required=True)
    username = forms.CharField(label="Nome de usuário", max_length=30, required=True)

    ALLOWED_DOMAINS = {
        'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com', 'icloud.com',
        'live.com', 'aol.com', 'bol.com.br', 'uol.com.br', 'protonmail.com'
    }

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('@')[-1].lower()
        
        if domain not in self.ALLOWED_DOMAINS:
            raise forms.ValidationError(
                "Por favor, use um e-mail de um provedor popular."
            )
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este e-mail já está cadastrado. Use outro e-mail ou faça login."
            )
        
        return email

    def clean_username(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(username=email).exists():
            raise forms.ValidationError(
                "Este e-mail já está cadastrado. Use outro e-mail ou faça login."
            )
        return email 