from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=255, decimal_places=2)

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"

@receiver(post_save, sender=Product)
def create_product_inventory(sender, instance, created, **kwargs):
    if created:  # Verifica se o produto foi recém-criado
        Inventory.objects.create(product=instance, quantity=0)

@receiver(post_save, sender=Transaction)
def update_product_inventory(sender, instance, created, **kwargs):
    if created:
        inventory = Inventory.objects.get(product=instance.product)
        old_quantity = inventory.quantity
        inventory.quantity = instance.quantity + old_quantity
        inventory.save()
