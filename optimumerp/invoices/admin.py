from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["id", "sale_order", "emission_date"]
    search_fields = ["sale_order"]
    list_per_page = 25
    list_max_show_all = 1000