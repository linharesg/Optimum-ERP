from django.shortcuts import render, get_object_or_404
from .models import Invoice
from sales_order.models import SalesOrder, SalesOrderProduct
from clients.models import Clients
from random import randint

def open_invoice(request, id):
    sale_order = get_object_or_404(SalesOrder, pk=id)
    sale_order_products = SalesOrderProduct.objects.filter(sale_order=sale_order)
    invoice = Invoice.objects.get(sale_order=sale_order)
    access_key = f"{randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)} \
        {randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)}"
    barcode = f"{randint(100000000, 999999999)}"
    context = {
        "sales_order": sale_order,
        "sale_order_products": sale_order_products,
        "invoice": invoice,
        "access_key": access_key,
        "barcode": barcode
        }
    
    return render(request, "invoices/invoice.html", context)