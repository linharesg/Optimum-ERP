from django.contrib import admin
from .models import SalesOrder, SalesOrderProduct


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    """
    Administração dos pedidos de venda.

    Attributes:
        list_display (list): Campos a serem exibidos na lista de pedidos.
        ordering (list): Campos pelos quais os pedidos serão ordenados.
        list_filter (list): Campos pelos quais os pedidos podem ser filtrados.
        search_fields (list): Campos pelos quais os pedidos podem ser pesquisados.
        list_display_links (list): Campos que servem como links na lista de pedidos.
        list_per_page (int): Número de itens exibidos por página na lista de pedidos.
        list_max_show_all (int): Número máximo de itens a serem exibidos na lista de pedidos.
    """
    list_display = ["id", "status", "created_at"]
    ordering = ["-id"]
    list_filter = ["id", "created_at"]
    search_fields = ["id"]
    list_display_links = ["id"]
    list_per_page = 25
    list_max_show_all = 1000

@admin.register(SalesOrderProduct)
class SalesOrderProductAdmin(admin.ModelAdmin):
    """
    Administração dos produtos dos pedidos de venda.

    Attributes:
        list_per_page (int): Número de itens exibidos por página na lista de produtos dos pedidos.
        list_max_show_all (int): Número máximo de itens a serem exibidos na lista de produtos dos pedidos.
    """
    list_per_page = 25
    list_max_show_all = 1000