from django.contrib import admin
from .models import Operacao, EmailConfirmationToken, UserProfile

admin.site.register(Operacao)
admin.site.register(EmailConfirmationToken)
admin.site.register(UserProfile)
