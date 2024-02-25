from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from .models import Employee
from django.db import transaction

User = get_user_model()

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "name"]

    def clean_password(self):
        password1 = self.cleaned_data.get["password1"]
        password2 = self.cleaned_data.get["password2"]
        if password1 != password2 and password1 != password2:
            raise ValidationError("As senhas não combinam.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "name", "is_active", "is_superuser"]


class UserForm(forms.ModelForm):
    groups = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    
    class Meta:
        model = User
        fields = ["name", "email", "password", "is_active"]
        widgets = {
            "password": forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @transaction.atomic
    def save(self, commit=True):
        password = self.cleaned_data.get("password")
        user = super().save(commit=False)

        # Hash da senha
        if password:
            user.set_password(password)
        if commit:
            user.save()
            group = self.cleaned_data.get("groups")
            # Cria um novo funcionário (Employee) associado ao usuário
            employee = Employee.objects.create(group=group)
            employee.user = user  # Define o usuário associado ao funcionário
            employee.save()
            user.groups.add(group)
        return user
