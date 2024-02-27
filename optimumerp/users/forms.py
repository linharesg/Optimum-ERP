from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from .models import Employee
from django.db import transaction

User = get_user_model()

class UserCreationForm(forms.ModelForm):
    """
    Formulário para criar um novo usuário.

    Atributos:
        password1 (str): Campo para a senha do usuário.
        password2 (str): Campo para a confirmação da senha do usuário.

    Métodos:
        clean_password: Valida se as senhas digitadas são iguais.
        save: Salva o usuário no banco de dados com a senha criptografada.
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "name"]

    def clean_password(self):
        """
        Verifica se as senhas digitadas nos campos 'password1' e 'password2' são iguais.
        """
        password1 = self.cleaned_data.get["password1"]
        password2 = self.cleaned_data.get["password2"]
        if password1 != password2 and password1 != password2:
            raise ValidationError("As senhas não combinam.")
        return password2
    
    def save(self, commit=True):
        """
        Salva o usuário com a senha criptografada.

        Args:
            commit (bool): Define se a operação de salvamento no banco de dados deve ser executada imediatamente.

        Returns:
            User: O objeto de usuário recém-criado.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):
    """
    Formulário para alterar os dados de um usuário.

    Atributos:
        password (ReadOnlyPasswordHashField): Campo somente leitura para a senha do usuário.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "name", "is_active", "is_superuser"]


class UserForm(forms.ModelForm):
    """
    Formulário para editar os dados de um usuário.

    Métodos:
        save: Salva o usuário, atribui automaticamente um grupo padrão e cria um novo funcionário associado.

    """

    class Meta:
        model = User
        fields = ["name", "email", "password", "is_active"]
        widgets = {
            "password": forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_group = Group.objects.get(name='Employee')

    @transaction.atomic
    def save(self, commit=True):
        """
        Salva o usuário, atribui automaticamente um grupo padrão e cria um novo funcionário associado.

        Args:
            commit (bool): Define se a operação de salvamento no banco de dados deve ser executada imediatamente.

        Returns:
            User: O objeto de usuário salvo.
        """
        password = self.cleaned_data.get("password")
        user = super().save(commit=False)

        # Hash da senha
        if password:
            user.set_password(password)
        if commit:
            user.save()
            # Atribui automaticamente o grupo padrão ao usuário
            user.groups.add(self.default_group)
            # Cria um novo funcionário (Employee) associado ao usuário e ao grupo padrão
            employee = Employee.objects.create(user=user, group=self.default_group)
            employee.save()
        return user