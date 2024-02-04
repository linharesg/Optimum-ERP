from django.contrib import admin
from .models import Suppliers


@admin.register(Suppliers)
class ProductsAdmin(admin.ModelAdmin):
    exclude = ["slug"]
