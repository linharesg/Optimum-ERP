from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    """
    Admin personalizado para o modelo de usuário personalizado.

    Atributos:
        form: A classe do formulário utilizado para editar usuários.
        add_form: A classe do formulário utilizado para adicionar usuários.
        fieldsets: Uma lista de tuplas que define os campos exibidos e agrupados no formulário de edição.
        add_fieldsets: Uma lista de tuplas que define os campos exibidos no formulário de criação.
        list_display: Uma lista de nomes de campos exibidos na lista de usuários no painel de administração.
        ordering: Uma lista de nomes de campos usada para definir a ordem de classificação padrão para a lista de usuários.
    """
    form = UserChangeForm
    add_form = UserCreationForm
    
    # Define os campos exibidos e agrupados no formulário de edição do usuário
    fieldsets = [
        (None, {"fields": ["email", "password"]}),  # Seção principal
        ("Informações pessoais", {"fields": ["name"]}),  # Seção de informações pessoais
        ("Permissões", {"fields": ["is_superuser", "groups", "user_permissions"]}),  # Seção de permissões
    ]

    # Define os campos exibidos no formulário de criação de usuário
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        ),
    ]

    # Define as colunas exibidas na lista de usuários no painel de administração
    list_display = ["name", "email", "is_superuser"]

    # Define a ordem de classificação padrão para a lista de usuários
    ordering = ["-id"]

# Registra o modelo de usuário personalizado no painel de administração com o admin personalizado
admin.site.register(User, UserAdmin)