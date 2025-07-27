from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta
from .models import Operacao, Calculadora, EmailConfirmationToken, UserProfile
from .forms import EmailUserCreationForm
import ast
import uuid

BASE_URL = "http://127.0.0.1:8000"
HISTORICO_LIMITE = 5
TEMPO_TOLERANCIA_REPETICAO = 5  # segundos
OPERADORES_VALIDOS = '+-*/'

def register_view(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 
                f'Conta criada com sucesso! Verifique seu email ({user.email}) para confirmar sua conta.')
            return redirect('login')
    else:
        form = EmailUserCreationForm()
    return render(request, 'Calculatorapp/register.html', {'form': form})

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_active=True)
            
            token = str(uuid.uuid4())
            
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.reset_token = token
            profile.save()
            
            reset_url = f"{BASE_URL}/reset-password/{token}/"
            
            html_message = render_to_string('Calculatorapp/email_reset_password.html', {
                'user': user,
                'reset_url': reset_url,
                'token': token
            })
            
            try:
                send_mail(
                    subject='Reset de Senha - Calculadora KOGUI',
                    message=strip_tags(html_message),
                    from_email='noreply@calculadora-kogui.com',
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                messages.success(request, f'Email de reset enviado para {email}')
            except Exception as e:
                messages.error(request, 'Erro ao enviar email. Tente novamente.')
                
        except User.DoesNotExist:
            messages.error(request, 'Email não encontrado ou conta não confirmada.')
    
    return render(request, 'Calculatorapp/forgot_password.html')

def reset_password_confirm_view(request, token):
    try:
        profile = UserProfile.objects.get(reset_token=token)
        user = profile.user
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password == confirm_password and len(new_password) >= 8:
                user.set_password(new_password)
                user.save()
                
                profile.reset_token = None
                profile.save()
                
                messages.success(request, 'Senha alterada com sucesso! Faça login com a nova senha.')
                return redirect('login')
            else:
                messages.error(request, 'Senhas não coincidem ou são muito curtas.')
        
        return render(request, 'Calculatorapp/reset_password_confirm.html', {'token': token})
        
    except UserProfile.DoesNotExist:
        messages.error(request, 'Link de reset inválido ou expirado.')
        return redirect('login')

def confirm_email_view(request, token):
    try:
        token_obj = get_object_or_404(EmailConfirmationToken, token=token, is_used=False)
        
        if token_obj.is_expired():
            messages.error(request, 'Link de confirmação expirado. Solicite um novo.')
            return redirect('login')
        
        user = token_obj.user
        user.is_active = True
        user.save()
        
        token_obj.is_used = True
        token_obj.save()
        
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.email_verified = True
        profile.save()
        
        messages.success(request, 'Email confirmado com sucesso! Agora você pode fazer login.')
        return redirect('login')
        
    except Exception as e:
        messages.error(request, 'Erro ao confirmar email. Tente novamente.')
        return redirect('login')

def resend_confirmation_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_active=False)
            
            EmailConfirmationToken.objects.filter(user=user, is_used=False).delete()
            
            token = EmailConfirmationToken.objects.create(user=user)
            confirmation_url = f"{BASE_URL}/confirm-email/{token.token}/"
            
            html_message = render_to_string('Calculatorapp/email_confirmation.html', {
                'user': user,
                'confirmation_url': confirmation_url,
                'token': token
            })
            
            try:
                send_mail(
                    subject='Confirme seu email - Calculadora KOGUI',
                    message=strip_tags(html_message),
                    from_email='noreply@calculadora-kogui.com',
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                messages.success(request, f'Novo email de confirmação enviado para {email}')
            except Exception as e:
                messages.error(request, 'Erro ao enviar email. Tente novamente.')
            
        except User.DoesNotExist:
            messages.error(request, 'Email não encontrado ou já confirmado.')
    
    return render(request, 'Calculatorapp/resend_confirmation.html')

def home_redirect(request):
    return redirect('login')

@login_required
@require_POST
def limpar_historico(request):
    Operacao.objects.filter(usuario=request.user).delete()
    return HttpResponseRedirect(reverse('calculator'))

@method_decorator(login_required, name='dispatch')
class CalculadoraView(View):
    template_name = 'Calculatorapp/calculator.html'

    def get(self, request):
        operacoes = Operacao.objects.filter(usuario=request.user)[:HISTORICO_LIMITE]
        return render(request, self.template_name, {'operacoes': operacoes})

    def post(self, request):
        expressao = request.POST.get('expressao', '').strip()
        a = request.POST.get('a')
        b = request.POST.get('b')
        operacao = request.POST.get('operacao')
        
        resultado_display, erro = self._processar_expressao(request, expressao, a, b, operacao)
        operacoes = Operacao.objects.filter(usuario=request.user)[:HISTORICO_LIMITE]
        
        return render(request, self.template_name, {
            'resultado_display': resultado_display,
            'erro': erro,
            'operacoes': operacoes,
            'a': a or '',
            'b': b or '',
            'operacao_selecionada': operacao
        })

    def _verificar_operacao_repetida(self, request, parametros, resultado):
        """Verifica se a operação já foi registrada recentemente"""
        ultima_operacao = Operacao.objects.filter(
            usuario=request.user,
            parametros=parametros,
            resultado=str(resultado)
        ).order_by('-dt_inclusao').first()
        
        # Só registra se não for a mesma operação da última vez
        return not ultima_operacao or ultima_operacao.dt_inclusao < timezone.now() - timedelta(seconds=TEMPO_TOLERANCIA_REPETICAO)

    def _registrar_operacao(self, request, parametros, resultado):
        """Registra operação se não for repetida"""
        if self._verificar_operacao_repetida(request, parametros, resultado):
            Operacao.objects.create(
                usuario=request.user,
                parametros=parametros,
                resultado=str(resultado)
            )

    def _processar_expressao(self, request, expressao, a, b, operacao):
        if expressao:
            return self._avaliar_expressao_completa(request, expressao)
        elif a and b and operacao:
            return self._avaliar_operacao_simples(request, a, b, operacao)
        return None, None

    def _avaliar_expressao_completa(self, request, expressao):
        try:
            if not expressao.strip():
                return None, "Expressão vazia"
            
            tree = ast.parse(expressao, mode='eval')
            for node in ast.walk(tree):
                if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, 
                                       ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div, 
                                       ast.Pow, ast.USub, ast.UAdd, ast.Mod, ast.Constant)):
                    raise ValueError('Expressão contém caracteres não permitidos')
            
            resultado = eval(compile(tree, filename="<ast>", mode="eval"), {"__builtins__": {}})
            resultado_display = int(resultado) if isinstance(resultado, float) and resultado.is_integer() else resultado
            
            if any(op in expressao for op in OPERADORES_VALIDOS):
                self._registrar_operacao(request, expressao, resultado_display)
            
            return resultado_display, None
        except ZeroDivisionError:
            return None, "Divisão por zero não permitida"
        except ValueError as e:
            return None, f"Expressão inválida: {e}"
        except Exception as e:
            return None, f"Erro inesperado: {e}"

    def _avaliar_operacao_simples(self, request, a, b, operacao):
        try:
            calc = Calculadora()
            a_float, b_float = calc.validar_operandos(a, b)
            
            simbolos = {'soma': '+', 'subtracao': '-', 'multiplicacao': '*', 'divisao': '/'}
            resultado = calc.calcular(operacao, a_float, b_float)
            resultado_display = calc.formatar_resultado(resultado)
            
            parametros = f"{a} {simbolos[operacao]} {b}"
            self._registrar_operacao(request, parametros, resultado_display)
            
            return resultado_display, None
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, f"Erro inesperado: {e}"