from django.db import models
from sales_order.models import SalesOrder

class Invoice(models.Model):
    sale_order = models.ForeignKey(SalesOrder, on_delete=models.DO_NOTHING)
    emission_date = models.DateTimeField(auto_now_add=True)
    