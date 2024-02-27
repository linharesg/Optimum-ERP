from decimal import Decimal
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from clients.models import Clients
from products.models import Product
from users.forms import User

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class SalesOrder(models.Model):
    """
    Representa um pedido de venda.

    Attributes:
        STATUS_CHOICES (dict): Dicionário contendo as opções de status do pedido.
        status (str): Status atual do pedido.
        delivery_date (DateField): Data de entrega do pedido.
        total_value (DecimalField): Valor total do pedido.
        discount (DecimalField): Desconto aplicado ao pedido em porcentagem.
        installments (IntegerField): Número de parcelas do pagamento.
        user (ForeignKey): Usuário responsável pelo pedido.
        created_at (DateTimeField): Data e hora de criação do pedido.
        client (ForeignKey): Cliente associado ao pedido.
        products (ManyToManyField): Produtos incluídos no pedido.
    """
    STATUS_CHOICES = {
        "Confirmado": "Confirmado",
        "Pendente": "Pendente",
        "Cancelado": "Cancelado"
    }
    
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    delivery_date = models.DateField(null=True, blank=True)
    total_value = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=3, decimal_places=0, default=Decimal(0), validators=PERCENTAGE_VALIDATOR)
    installments = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(36)])
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Clients, on_delete=models.PROTECT)
    products = models.ManyToManyField(
        Product,
        through="SalesOrderProduct",
        through_fields=("sale_order", "product"),
        blank=False
    )
    
    class Meta:
        verbose_name = "Pedido de venda"
        verbose_name_plural = "Pedidos de venda"

    def __str__(self):
        return f"{self.id}"

class SalesOrderProduct(models.Model):
    """
    Representa um produto incluído em um pedido de venda.

    Attributes:
        product (ForeignKey): Produto associado ao item do pedido.
        sale_order (ForeignKey): Pedido de venda ao qual o produto pertence.
        unit_value (DecimalField): Valor unitário do produto.
        amount (DecimalField): Quantidade do produto.
        total_value_product (DecimalField): Valor total do item do pedido.
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sale_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    unit_value = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01, message='Informe um valor válido')])
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01, message='Informe um valor válido')])
    total_value_product = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01, message='Informe um valor válido')])
    
    class Meta:
        verbose_name = "Produto do pedido de venda"
        verbose_name_plural = "Produtos do pedido de venda"
        unique_together = [["product", "sale_order"]]
        
    def __str__(self):
        return f"Pedido: {self.sale_order} | Item: {self.product}"