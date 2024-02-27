from decimal import Decimal
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from suppliers.models import Suppliers
from products.models import Product
from users.forms import User

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class Purchases(models.Model):
    """
    Modelo que representa um pedido de compra no sistema.

    Attributes:
        STATUS_CHOICES (dict): Escolhas possíveis para o status do pedido.
        status (str): O status atual do pedido.
        delivery_date (DateField): A data de entrega do pedido.
        total_value (DecimalField): O valor total do pedido.
        discount (DecimalField): O desconto aplicado ao pedido.
        installments (IntegerField): O número de parcelas do pagamento.
        user (ForeignKey): O usuário que criou o pedido.
        created_at (DateTimeField): A data e hora de criação do pedido.
        supplier (ForeignKey): O fornecedor associado ao pedido.
        products (ManyToManyField): Os produtos associados ao pedido.
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Suppliers, on_delete=models.PROTECT)
    products = models.ManyToManyField(
        Product,
        through="PurchasesProduct",
        through_fields=("purchase", "product"),
        blank=False
    )
    
    class Meta:
        verbose_name = "Pedido de compra"
        verbose_name_plural = "Pedidos de compra"

    def __str__(self):
        return f"{self.id}"
    

class PurchasesProduct(models.Model):
    """
    Modelo que representa um produto associado a um pedido de compra.

    Attributes:
        product (ForeignKey): O produto associado.
        purchase (ForeignKey): O pedido de compra associado.
        unit_value (DecimalField): O valor unitário do produto.
        amount (DecimalField): A quantidade do produto.
        total_value_product (DecimalField): O valor total do produto no pedido.
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    purchase = models.ForeignKey(Purchases, on_delete=models.CASCADE)
    unit_value = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01, message='Informe um valor válido')])
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01, message='Informe um valor válido')])
    total_value_product = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01, message='Informe um valor válido')])

    class Meta:
        verbose_name = "Produto do pedido de compra"
        verbose_name_plural = "Produtos do pedido de compra"
        unique_together = [["product", "purchase"]]
        
    def __str__(self):
        return f"Pedido: {self.purchase} | Item: {self.product}"