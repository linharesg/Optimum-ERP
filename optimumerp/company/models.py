from django.db import models
from django.utils.text import slugify

class Company(models.Model):
    """
    Este modelo contém informações sobre uma empresa, incluindo seu nome, nome fantasia, registro estadual,
    CNPJ, endereço, e detalhes de contato.

    Atributos:
        name (str): O nome da empresa.
        fantasy_name (str): O nome fantasia da empresa.
        state_registration (str): O registro estadual da empresa.
        slug (str): O slug gerado automaticamente para a empresa com base no nome fantasia.
        cnpj (str): O CNPJ (Cadastro Nacional da Pessoa Jurídica) da empresa.
        email (str): O endereço de e-mail da empresa.
        zipcode (str): O CEP (Código de Endereçamento Postal) da empresa.
        street (str): O nome da rua ou avenida onde a empresa está localizada.
        number (str): O número do endereço da empresa.
        city (str): A cidade onde a empresa está localizada.
        state (str): O estado onde a empresa está localizada, representado por uma sigla de duas letras.
        phone (str): O número de telefone da empresa.

    Métodos:
        __str__(): Retorna uma representação de string do nome da empresa.
        __repr__(): Retorna uma representação de string do nome da empresa.
        save(): Sobrescreve o método de salvar para gerar automaticamente o slug com base no nome fantasia.

    Meta:
        verbose_name (str): O nome legível para humanos do modelo no singular.
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
    
    name = models.CharField(max_length=255)
    fantasy_name = models.CharField(max_length=255, unique=True)
    state_registration = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    cnpj = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    zipcode = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    phone = models.CharField(max_length=255)
    
    def __str__(self):
        """
        Retorna uma representação de string do nome da empresa.
        """
        return self.name

    def __repr__(self):
        """
        Retorna uma representação de string do nome da empresa.
        """
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método de salvar para gerar automaticamente o slug com base no nome fantasia.
        """
        self.slug = slugify(self.fantasy_name)
        super(Company, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Empresa"