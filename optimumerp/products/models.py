from django.db import models
from django.utils.text import slugify
from suppliers.models import Suppliers

class InternalCode(models.Model):
    code = models.CharField(max_length=255, unique=True)
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class Product(models.Model):
    MEASUREMENT_CHOICES = {
        "KG": "Quilograma",
        "Metro": "Metro",
        "Litro": "Litro",
        "Unidade": "Unidade"
    }

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    minimum_stock = models.DecimalField(max_digits=255, decimal_places=2)
    maximum_stock = models.DecimalField(max_digits=255, decimal_places=2)
    internal_code = models.ForeignKey(InternalCode, on_delete=models.DO_NOTHING)
    sale_price = models.DecimalField(max_digits=255, decimal_places=2)
    expiration_date = models.DateField(null=True, blank=True)
    unit_of_measurement = models.CharField(max_length=7, choices=MEASUREMENT_CHOICES)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

class ProductInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    local = models.CharField(max_length=255)

    def __str__(self):
        return f"Produto: {self.product.name} | Quantidade: {self.quantity}"
    class Meta:
        verbose_name = "Estoque de produto"
        verbose_name_plural = "Estoque de produtos"
        unique_together = [["product", "local"]]

class SupplierProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Fornecedor do Produto"
        verbose_name_plural = "Fornecedores do Produto"
        unique_together = [["supplier", "product"]]