from django.contrib import admin
from .models import Suppliers


@admin.register(Suppliers)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["id", "company_name", "fantasy_name", "email", "enabled"]
    exclude = ["slug"]
    ordering = ["id"]
    list_filter = ["enabled", "created_at"]
    search_fields = ["company_name", "email"]
    list_display_links = ["company_name", "id"]
    list_editable = ["fantasy_name"]
    list_per_page = 25
    list_max_show_all = 1000