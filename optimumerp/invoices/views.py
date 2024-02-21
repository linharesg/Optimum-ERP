from django.shortcuts import redirect, render, get_object_or_404
from .models import Invoice
from sales_order.models import SalesOrder, SalesOrderProduct
from clients.models import Clients
from random import randint

def open_invoice(request, id):
    sale_order = get_object_or_404(SalesOrder, pk=id)
    sale_order_products = SalesOrderProduct.objects.filter(sale_order=sale_order)
    invoice = Invoice.objects.get(sale_order=sale_order)
    context = {
        "sale_order": sale_order,
        "sale_order_products": sale_order_products,
        "invoice": invoice
        }
    
    return render(request, "invoices/invoice.html", context)

def create_invoice(request, id):
    sale_order = get_object_or_404(SalesOrder, pk=id)
    try:
        invoice = Invoice.objects.get(sale_order=sale_order)
    except:
        sale_order = get_object_or_404(SalesOrder, pk=id)
        access_key = f"{randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)}\
            {randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)} {randint(1000, 9999)}"
        barcode = f"{randint(100000000, 999999999)}"
        Invoice.objects.create(sale_order=sale_order, access_key=access_key, barcode=barcode)
    
        return redirect("invoices:open_invoice", id=sale_order.id)
    return redirect("invoices:open_invoice", id=sale_order.id)