from django.db import models
from django.utils.text import slugify


class Suppliers(models.Model):
    """
    Modelo que representa fornecedores.

    Atributos:
        STATE_CHOICES (dict): Dicionário que mapeia siglas de estados para seus nomes completos.
        company_name (CharField): Nome da empresa.
        fantasy_name (CharField): Nome fantasia da empresa.
        slug (SlugField): Slug único para identificação do fornecedor na URL.
        representative (CharField): Nome do representante da empresa.
        cnpj (CharField): Número de CNPJ da empresa.
        email (EmailField): Endereço de e-mail da empresa.
        zipcode (CharField): Código postal (CEP) da empresa.
        street (CharField): Nome da rua do endereço da empresa.
        number (CharField): Número do endereço da empresa.
        city (CharField): Cidade do endereço da empresa.
        state (CharField): Estado do endereço da empresa (sigla).
        phone (CharField): Número de telefone da empresa.
        enabled (BooleanField): Indica se o fornecedor está ativo ou não.
        created_at (DateTimeField): Data e hora de criação do registro.

    Métodos:
        __str__(): Retorna uma representação de string do fornecedor.
        __repr__(): Retorna uma representação de string do fornecedor.
        save(*args, **kwargs): Sobrescreve o método save para gerar automaticamente o slug do fornecedor.

    Meta:
        verbose_name (str): Nome amigável singular para o modelo no admin do Django.
        verbose_name_plural (str): Nome amigável plural para o modelo no admin do Django.
    """
    
    STATE_CHOICES = {
        "AC": "Acre",
        "AL": "Alagoas",
        "AP": "Amapá",
        "AM": "Amazonas",
        "BA": "Bahia",
        "CE": "Ceará",
        "ES": "Espírito Santo",
        "GO": "Goiás",
        "MA": "Maranhão",
        "MT": "Mato Grosso",
        "MS": "Mato Grosso do Sul",
        "MG": "Minas Gerais",
        "PA": "Pará",
        "PB": "Paraíba",
        "PR": "Paraná",
        "PE": "Pernambuco",
        "PI": "Piauí",
        "RJ": "Rio de Janeiro",
        "RN": "Rio Grande do Norte",
        "RS": "Rio Grande do Sul",
        "RO": "Rondônia",
        "RR": "Roraima",
        "SC": "Santa Catarina",
        "SP": "São Paulo",
        "SE": "Sergipe",
        "TO": "Tocantins",
        "DF": "Distrito Federal",
    }
    
    company_name = models.CharField(max_length=255)
    fantasy_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    representative = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    zipcode = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    phone = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """
        Retorna uma representação de string do fornecedor.
        """
        return self.company_name

    def __repr__(self):
        """
        Retorna uma representação de string do fornecedor.
        """
        return self.company_name
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para gerar automaticamente o slug do fornecedor.
        """
        self.slug = slugify(self.fantasy_name)
        super(Suppliers, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"