# 🧮 Calculadora KOGUI

Uma calculadora web desenvolvida em Django com sistema de autenticação e histórico de operações.

## ✨ Funcionalidades

- **Calculadora Completa**: Operações básicas (soma, subtração, multiplicação, divisão)
- **Expressões Matemáticas**: Suporte a expressões complexas com validação de segurança
- **Sistema de Autenticação**: Registro, login e confirmação por email
- **Histórico de Operações**: Armazenamento das últimas 5 operações por usuário
- **Prevenção de Duplicatas**: Evita registrar operações repetidas em sequência
- **Reset de Senha**: Sistema completo de recuperação de senha
- **Interface Responsiva**: Design moderno e adaptável

## 🏗️ Arquitetura

### Padrão MVT (Model-View-Template)
- **Models**: `Operacao`, `EmailConfirmationToken`, `UserProfile`, `Calculadora`
- **Views**: Class-Based Views e Function-Based Views
- **Templates**: HTML5 com CSS3 e JavaScript

### Estrutura do Projeto
```
Calculadora_Teste_KOGUI/
├── app/                    # Configurações do Django
├── Calculatorapp/          # Aplicação principal
│   ├── models.py          # Modelos de dados
│   ├── views.py           # Lógica de negócio
│   ├── forms.py           # Formulários customizados
│   ├── templates/         # Templates HTML
│   └── urls.py            # Roteamento
├── manage.py              # Script de gerenciamento
└── requirements.txt       # Dependências
```

## 🚀 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/calculadora-kogui.git
cd calculadora-kogui
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Execute o servidor**
```bash
python manage.py runserver
```

6. **Acesse a aplicação**
```
http://127.0.0.1:8000
```

## 📋 Configurações

### Variáveis de Ambiente
- `EMAIL_BACKEND`: Configurado para console (desenvolvimento)
- `BASE_URL`: URL base para links de email

### Configurações de Email
- Domínios permitidos: Gmail, Hotmail, Outlook, Yahoo, etc.
- Tokens de confirmação com expiração de 24h
- Sistema de reset de senha com tokens únicos

## 🎯 Funcionalidades Técnicas

### Segurança
- **Validação de Expressões**: Uso do módulo `ast` para prevenir execução de código malicioso
- **CSRF Protection**: Proteção contra ataques CSRF
- **Email Validation**: Validação de domínios de email
- **Token Security**: Tokens únicos para confirmação e reset

### Performance
- **Prevenção de Duplicatas**: Evita registrar operações repetidas em 5 segundos
- **Queries Otimizadas**: Filtros eficientes no banco de dados
- **Cache de Operações**: Histórico limitado a 5 operações por usuário

### Lógica de Negócio
- **Classe Calculadora**: Implementação orientada a objetos
- **Método `calcular()`**: Centraliza operações matemáticas
- **Validação de Divisão por Zero**: Tratamento específico de erro
- **Formatação de Resultados**: Conversão automática de floats para int

## 🧪 Testes

### Funcionalidades Testadas
- ✅ Registro de usuário com validação de email
- ✅ Confirmação de email com tokens
- ✅ Login e logout
- ✅ Reset de senha
- ✅ Operações matemáticas básicas
- ✅ Expressões matemáticas complexas
- ✅ Histórico de operações
- ✅ Prevenção de operações duplicadas
- ✅ Validação de segurança em expressões

## 🔧 Tecnologias Utilizadas

- **Backend**: Django 5.2.4
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento)
- **Autenticação**: Django Auth System
- **Email**: Django Email Backend
- **Segurança**: CSRF, AST Validation

## 📊 Estrutura de Dados

### Modelo Operacao
```python
class Operacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    parametros = models.CharField(max_length=100)
    resultado = models.CharField(max_length=100)
    dt_inclusao = models.DateTimeField(default=timezone.now)
```

### Classe Calculadora
```python
class Calculadora:
    def calcular(self, operacao, a, b):
        operacoes = {
            'soma': self.somar,
            'subtracao': self.subtrair,
            'multiplicacao': self.multiplicar,
            'divisao': self.dividir
        }
        return operacoes[operacao](a, b)
```

## 🎨 Interface

### Características do Design
- **Responsivo**: Adaptável a diferentes tamanhos de tela
- **Moderno**: Interface limpa e intuitiva
- **Acessível**: Navegação clara e feedback visual
- **Interativo**: Botões com feedback visual

## 🔒 Segurança

### Implementações de Segurança
- **Validação AST**: Previne execução de código malicioso
- **CSRF Protection**: Proteção contra ataques cross-site
- **Email Validation**: Validação de domínios permitidos
- **Token Security**: Tokens únicos e com expiração
- **Input Sanitization**: Limpeza e validação de entrada

## 📈 Melhorias Implementadas

### Funcionalidades Adicionadas
- ✅ **Prevenção de Duplicatas**: Evita registrar operações repetidas
- ✅ **Validação de Expressões**: Segurança contra código malicioso
- ✅ **Sistema de Email**: Confirmação e reset de senha
- ✅ **Histórico Inteligente**: Limitação e prevenção de duplicatas
- ✅ **Interface Melhorada**: Design responsivo e moderno

### Otimizações Técnicas
- ✅ **Métodos Privados**: Organização do código em métodos específicos
- ✅ **Tratamento de Erros**: Mensagens específicas para cada tipo de erro
- ✅ **Validação Robusta**: Verificações de entrada mais rigorosas
- ✅ **Performance**: Queries otimizadas e cache eficiente

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- Django Documentation
- Comunidade KOGUI
- Tutoriais e recursos educacionais utilizados 