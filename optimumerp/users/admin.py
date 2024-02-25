from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Informações pessoais", {"fields": ["name"]}),
        ("Permissões", {"fields": ["is_superuser", "groups", "user_permissions"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        ),
    ]

    list_display = ["name", "email", "is_superuser"]
    ordering = ["-id"]

admin.site.register(User, UserAdmin)