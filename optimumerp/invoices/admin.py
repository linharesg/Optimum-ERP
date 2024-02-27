from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Admin personalizado para o modelo de fatura.

    Este admin define como as faturas serão exibidas e filtradas no painel de administração.

    Atributos:
        list_display (list): Lista de campos a serem exibidos na lista de faturas.
        search_fields (list): Lista de campos pelos quais as faturas podem ser pesquisadas.
        list_per_page (int): Número de faturas exibidas por página na lista de administração.
        list_max_show_all (int): Número máximo de faturas que podem ser exibidas em uma única página na lista de administração.
    """
    list_display = ["id", "sale_order", "emission_date"]
    search_fields = ["sale_order"]
    list_per_page = 25
    list_max_show_all = 1000