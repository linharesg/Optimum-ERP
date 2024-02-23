from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_per_page = 1
    list_max_show_all = 1000
    list_display = ["id", "name", "fantasy_name", "email"]
    exclude = ["slug"]
    ordering = ["id"]
    list_display_links = ["name", "id"]
    list_editable = ["fantasy_name"]
    list_per_page = 1
    list_max_show_all = 1