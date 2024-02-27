from django.contrib import admin
from .models import Suppliers


@admin.register(Suppliers)
class ProductsAdmin(admin.ModelAdmin):
    """
    Admin personalizado para o modelo de fornecedores.

    Atributos:
        list_display (list): Lista de campos a serem exibidos na lista de fornecedores no painel de administração.
        exclude (list): Lista de campos a serem excluídos do formulário de administração.
        ordering (list): Lista de campos utilizados para ordenar a lista de fornecedores.
        list_filter (list): Lista de campos pelos quais os fornecedores podem ser filtrados.
        search_fields (list): Lista de campos pelos quais os fornecedores podem ser pesquisados.
        list_display_links (list): Lista de campos que são exibidos como links na lista de fornecedores.
        list_editable (list): Lista de campos que podem ser editados diretamente na lista de fornecedores.
        list_per_page (int): Número de fornecedores exibidos por página na lista de fornecedores.
        list_max_show_all (int): Número máximo de fornecedores exibidos quando a opção "Mostrar todos" é selecionada.
    """
    list_display = ["id", "company_name", "fantasy_name", "email", "enabled"]
    exclude = ["slug"]
    ordering = ["id"]
    list_filter = ["enabled", "created_at"]
    search_fields = ["company_name", "email"]
    list_display_links = ["company_name", "id"]
    list_editable = ["fantasy_name"]
    list_per_page = 25
    list_max_show_all = 1000