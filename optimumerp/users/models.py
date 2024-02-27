from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group

class UserManager(BaseUserManager):
    """
    Gerenciador de usuário personalizado onde os e-mails são os identificadores exclusivos para autenticação,
    ao invés de nomes de usuário.

    Métodos:
        create_user: Cria e salva um usuário com o e-mail, nome e senha fornecidos.
        create_superuser: Cria e salva um superusuário com o e-mail, nome e senha fornecidos.
    """
    def create_user(self, email, name, password=None):
        """
        Cria e salva um usuário com o e-mail, nome e senha fornecidos.

        Args:
            email (str): E-mail do usuário.
            name (str): Nome do usuário.
            password (str): Senha do usuário.

        Returns:
            User: O objeto de usuário recém-criado.

        Raises:
            ValueError: Se nenhum e-mail for fornecido.
        """
        if not email:
            raise ValueError("Por favor, informe um e-mail.")
        
        user = self.model(email=self.normalize_email(email), name=name,)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, name, password=None):
        """
        Cria e salva um superusuário com o e-mail, nome e senha fornecidos.

        Args:
            email (str): E-mail do superusuário.
            name (str): Nome do superusuário.
            password (str): Senha do superusuário.

        Returns:
            User: O objeto de superusuário recém-criado.
        """
        user = self.create_user(email, password=password, name=name)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuário personalizado onde os e-mails são os identificadores exclusivos para autenticação,
    ao invés de nomes de usuário.

    Atributos:
        email (str): E-mail do usuário (único).
        name (str): Nome do usuário.
        password (str): Senha do usuário.
        is_staff (bool): Indica se o usuário pode acessar a interface de administração.
        is_active (bool): Indica se o usuário está ativo.

    Métodos:
        __str__: Retorna uma representação de string do usuário.
    """
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
        """
        Retorna uma representação de string do usuário.
        """
        return self.name
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


class Employee(models.Model):
    """
    Modelo que representa um funcionário associado a um usuário.

    Atributos:
        group (Group): Grupo ao qual o funcionário está associado.
        user (User): Usuário associado ao funcionário.

    Métodos:
        __str__: Retorna uma representação de string do funcionário.
    """
    DEFAULT_GROUP_ID = 1
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=DEFAULT_GROUP_ID)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Retorna uma representação de string do funcionário.
        """
        return self.user.name if self.user else "Employee"

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"