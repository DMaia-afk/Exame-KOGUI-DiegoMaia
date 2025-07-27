from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from datetime import timedelta

class Calculadora:
    def somar(self, a, b):
        return a + b
    
    def subtrair(self, a, b):
        return a - b
    
    def multiplicar(self, a, b):
        return a * b
    
    def dividir(self, a, b):
        if b == 0:
            raise ValueError("Divisão por zero não permitida")
        return a / b
    
    def calcular(self, operacao, a, b):
        operacoes = {
            'soma': self.somar,
            'subtracao': self.subtrair,
            'multiplicacao': self.multiplicar,
            'divisao': self.dividir
        }
        
        if operacao not in operacoes:
            raise ValueError(f"Operação '{operacao}' não suportada")
        
        return operacoes[operacao](a, b)

class Operacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    parametros = models.CharField(max_length=100)
    resultado = models.CharField(max_length=100)
    dt_inclusao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.parametros} = {self.resultado} (por {self.usuario.username})"

class EmailConfirmationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=24)
    
    def __str__(self):
        return f"Token para {self.user.email} - {'Usado' if self.is_used else 'Pendente'}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"Perfil de {self.user.email} - {'Verificado' if self.email_verified else 'Não verificado'}"


