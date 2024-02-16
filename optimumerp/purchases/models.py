from decimal import Decimal
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from suppliers.models import Suppliers
from products.models import Product
PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

# Create your models here.
class Purchases(models.Model):
    
    STATUS_CHOICES = {
        "Confirmado": "Confirmado",
        "Pendente": "Pendente",
        "Cancelado": "Cancelado"
    }
    
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    delivery_date = models.DateField(null=True, blank=True)
    total_value = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=3, decimal_places=0, default=Decimal(0), validators=PERCENTAGE_VALIDATOR)
    installments = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(36)])
    ############# USUARIO: CRIAR RELAÇÃO COM O USUARIO QUE EMITIU O PEDIDO #########################
    created_at = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
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
    
    def save(self, *args, **kwargs):
        self.status = "Confirmado"
        super(Purchases, self).save(*args, **kwargs)
        
class PurchasesProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ######## ESTOQUE: CRIAR RELAÇÃO COM OS LOCAIS DE ESTOQUE ######################################
    purchase = models.ForeignKey(Purchases, on_delete=models.CASCADE)
    unit_value = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Produto do pedido de compra"
        verbose_name_plural = "Produtos do pedido de compra"
        unique_together = [["product", "purchase"]]
        
    def __str__(self):
        return f"Pedido: {self.purchase} | Item: {self.product}"