from django.contrib import admin
from .models import SalesOrder, SalesOrderProduct


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ["id","status", "created_at"]
    ordering = ["-id"]
    list_filter = ["id", "created_at"]
    search_fields = ["id"]
    list_display_links = ["id"]
    list_per_page = 25
    list_max_show_all = 1000
    
@admin.register(SalesOrderProduct)
class SalesOrderProductAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_max_show_all = 1000