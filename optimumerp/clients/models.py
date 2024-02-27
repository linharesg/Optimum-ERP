from django.db import models
from django.utils.text import slugify


class Clients(models.Model):
    """
    Modelo que representa um cliente.

    Este modelo contém informações sobre os clientes, incluindo seu nome empresarial, nome fantasia, CNPJ, e-mail,
    endereço, telefone, entre outros.

    Attributes:
        STATE_CHOICES (dict): Um dicionário que mapeia os códigos de estado do Brasil para seus respectivos nomes.
        company_name (str): Nome empresarial do cliente.
        fantasy_name (str): Nome fantasia do cliente.
        slug (str): Slug utilizado para URLs amigáveis.
        representative (str): Nome do representante do cliente.
        cnpj (str): CNPJ (Cadastro Nacional da Pessoa Jurídica) do cliente.
        email (str): Endereço de e-mail do cliente.
        zipcode (str): CEP (Código de Endereçamento Postal) do cliente.
        street (str): Nome da rua do endereço do cliente.
        number (str): Número do endereço do cliente.
        city (str): Nome da cidade do endereço do cliente.
        state (str): Estado do endereço do cliente, representado por um código de duas letras.
        phone (str): Número de telefone do cliente.
        enabled (bool): Indica se o cliente está ativo ou inativo.
        created_at (datetime): Data e hora de criação do registro do cliente.

    Methods:
        __str__(): Retorna uma representação de string do nome empresarial do cliente.
        __repr__(): Retorna uma representação de string do nome empresarial do cliente.
        save(*args, **kwargs): Sobrescreve o método save() para gerar o slug do cliente antes de salvar no banco de dados.

    Meta:
        verbose_name (str): Nome singular do modelo, utilizado no admin do Django.
        verbose_name_plural (str): Nome plural do modelo, utilizado no admin do Django.
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
        Retorna uma representação de string do nome empresarial do cliente.
        
        Returns:
            str: Nome empresarial do cliente.
        """
        return self.company_name

    def __repr__(self):
        """
        Retorna uma representação de string do nome empresarial do cliente.

        Returns:
            str: Nome empresarial do cliente.
        """
        return self.company_name
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save() para gerar o slug do cliente antes de salvar no banco de dados.

        Args:
            *args: Argumentos posicionais adicionais.
            **kwargs: Argumentos de palavra-chave adicionais.
        """
        self.slug = slugify(self.fantasy_name)
        super(Clients, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"