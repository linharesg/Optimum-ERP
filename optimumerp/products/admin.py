from django.contrib import admin
from .models import Product, SupplierProduct


@admin.register(Product)
class SalesOrderAdmin(admin.ModelAdmin):
    """
    Configuração do painel de administração para o modelo Product.
    
    Este painel de administração permite visualizar e gerenciar os produtos.
    """
    list_per_page = 25
    list_max_show_all = 1000
    

@admin.register(SupplierProduct)
class SalesOrderProductAdmin(admin.ModelAdmin):
    """
    Configuração do painel de administração para o modelo SupplierProduct.
    
    Este painel de administração permite visualizar e gerenciar os fornecedores de produtos.
    """    
    list_per_page = 25
    list_max_show_all = 1000