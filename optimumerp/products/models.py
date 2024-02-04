from django.db import models
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    MEASUREMENT_CHOICES = {
        "KG": "Quilograma",
        "Metro": "Metro",
        "Litro": "Litro",
        "Unidade": "Unidade"
    }
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    sale_price = models.FloatField()
    is_perishable = models.BooleanField()
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