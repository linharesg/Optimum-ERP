from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Por favor, informe um e-mail.")
        
        user = self.model(email=self.normalize_email(email), name=name,)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, password=password, name=name)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("E-mail", unique=True)
    name = models.CharField("Nome", max_length=255)
    password = models.CharField("Senha", max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField("Ativo", default=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


class Employee(models.Model):
    DEFAULT_GROUP_ID = 1
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=DEFAULT_GROUP_ID)

    def __str__(self):
        return self.user.name if self.user else "Employee"

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"