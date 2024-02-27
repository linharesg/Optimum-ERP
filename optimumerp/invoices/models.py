from django.db import models
from sales_order.models import SalesOrder

class Invoice(models.Model):
    """
    Modelo que representa uma fatura.

    Esta classe representa as informações relacionadas a uma fatura, incluindo detalhes do emissor, do destinatário
    e da venda associada.

    Atributos:
        sale_order (ForeignKey): Venda associada à fatura.
        access_key (CharField): Chave de acesso da fatura.
        barcode (CharField): Código de barras da fatura.
        emitter_name (CharField): Nome do emissor.
        emitter_fantasy_name (CharField): Nome fantasia do emissor.
        emitter_state_registration (CharField): Inscrição estadual do emissor.
        emitter_cnpj (CharField): CNPJ do emissor.
        emitter_email (EmailField): Email do emissor.
        emitter_zipcode (CharField): CEP do emissor.
        emitter_street (CharField): Rua do emissor.
        emitter_number (CharField): Número do emissor.
        emitter_city (CharField): Cidade do emissor.
        emitter_state (CharField): Estado do emissor.
        emitter_phone (CharField): Telefone do emissor.
        receiver_name (CharField): Nome do destinatário.
        receiver_fantasy_name (CharField): Nome fantasia do destinatário.
        receiver_cnpj (CharField): CNPJ do destinatário.
        receiver_email (EmailField): Email do destinatário.
        receiver_zipcode (CharField): CEP do destinatário.
        receiver_street (CharField): Rua do destinatário.
        receiver_number (CharField): Número do destinatário.
        receiver_city (CharField): Cidade do destinatário.
        receiver_state (CharField): Estado do destinatário.
        receiver_phone (CharField): Telefone do destinatário.
        emission_date (DateTimeField): Data de emissão da fatura.
    """
    sale_order = models.ForeignKey(SalesOrder, on_delete=models.DO_NOTHING)
    access_key = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255)
    emitter_name = models.CharField(max_length=255)
    emitter_fantasy_name = models.CharField(max_length=255)
    emitter_state_registration = models.CharField(max_length=255)
    emitter_cnpj = models.CharField(max_length=20)
    emitter_email = models.EmailField(max_length=255)
    emitter_zipcode = models.CharField(max_length=20)
    emitter_street = models.CharField(max_length=255)
    emitter_number = models.CharField(max_length=255)
    emitter_city = models.CharField(max_length=255)
    emitter_state = models.CharField(max_length=255)
    emitter_phone = models.CharField(max_length=255)
    receiver_name = models.CharField(max_length=255)
    receiver_fantasy_name = models.CharField(max_length=255)
    receiver_cnpj = models.CharField(max_length=20)
    receiver_email = models.EmailField(max_length=255)
    receiver_zipcode = models.CharField(max_length=20)
    receiver_street = models.CharField(max_length=255)
    receiver_number = models.CharField(max_length=255)
    receiver_city = models.CharField(max_length=255)
    receiver_state = models.CharField(max_length=255)
    receiver_phone = models.CharField(max_length=255)
    emission_date = models.DateTimeField(auto_now_add=True)
    