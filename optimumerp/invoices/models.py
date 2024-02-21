from django.db import models
from sales_order.models import SalesOrder

class Invoice(models.Model):
    sale_order = models.ForeignKey(SalesOrder, on_delete=models.DO_NOTHING)
    access_key = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255)
    emission_date = models.DateTimeField(auto_now_add=True)
    