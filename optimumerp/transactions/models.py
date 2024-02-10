from django.db import models
from products.models import Product

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = {
        "IN": "Entrada",
        "OUT": "Saída"
    }

    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=255, decimal_places=2)
    type = models.CharField(max_length=255, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Produto: {self.product} | Quantidade: {self.quantity} | Tipo: {self.type} | Data: {self.date}"
    
    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"