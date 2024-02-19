import decimal
from django.db import models
from products.models import Product
from inventory.models import Inventory
from django.contrib import messages
from django.db import transaction
from .exceptions import TransactionQuantityError
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = {
        "IN": "Entrada",
        "OUT": "Saída"
    }

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=255, decimal_places=2)
    type = models.CharField(max_length=255, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Produto: {self.product} | Quantidade: {self.quantity} | Tipo: {self.type} | Data: {self.date}"
    
    @classmethod
    def create(cls, product, quantity, type):
        inventory = Inventory.objects.get(product__id=product)
        with transaction.atomic():
            if type == "OUT":
                if inventory.quantity - quantity < 0:
                    transaction_error = TransactionQuantityError("Quantidade indisponível no estoque")
                    print(transaction_error)
                    raise transaction_error
                else:
                    inventory.quantity -= quantity
                    inventory.save()

            elif type == "IN":
                inventory.quantity += quantity
                inventory.save()

        

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
