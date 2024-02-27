from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Admin personalizado para o modelo de empresa.
    
    Este admin personalizado é usado para configurar a exibição e o comportamento do modelo de empresa
    no painel de administração do Django.

    Attributes:
        list_per_page (int): O número de objetos exibidos por página na visualização da lista.
        list_max_show_all (int): O número máximo de objetos que podem ser exibidos na visualização da lista sem paginação.
    """
    list_per_page = 1
    list_max_show_all = 1000
    list_display = ["id", "name", "fantasy_name", "email"]
    exclude = ["slug"]
    ordering = ["id"]
    list_display_links = ["name", "id"]
    list_editable = ["fantasy_name"]
    list_per_page = 1
    list_max_show_all = 1