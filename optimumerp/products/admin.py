from django.contrib import admin
from .models import Product, SupplierProduct


@admin.register(Product)
class SalesOrderAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_max_show_all = 1000
    
@admin.register(SupplierProduct)
class SalesOrderProductAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_max_show_all = 1000