from django.db import models
from products.models import Product

class Inventory(models.Model):
    """
    Modelo que representa o estoque de produtos.

    Atributos:
        product (ForeignKey): Chave estrangeira para o modelo Product, associando o item de inventário a um produto.
        quantity (DecimalField): Quantidade do produto em estoque, representada por um número decimal.

    Meta:
        verbose_name (str): O nome singular para este modelo utilizado em exibições administrativas.
        verbose_name_plural (str): O nome plural para este modelo utilizado em exibições administrativas.
    """

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=255, decimal_places=2)

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"