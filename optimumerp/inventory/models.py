from django.db import models
from products.models import Product

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=255, decimal_places=2)

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"
