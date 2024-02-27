from django.contrib import admin
from .models import Purchases, PurchasesProduct

@admin.register(Purchases)
class PurchasesAdmin(admin.ModelAdmin):
    list_display = ["id","status", "created_at"]
    ordering = ["id"]
    list_filter = ["id", "created_at"]
    search_fields = ["id"]
    list_display_links = ["id"]
    list_per_page = 25
    list_max_show_all = 1000
    
@admin.register(PurchasesProduct)
class PurchasesProductAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_max_show_all = 1000