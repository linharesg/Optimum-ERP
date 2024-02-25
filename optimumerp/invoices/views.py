from django.shortcuts import redirect, render, get_object_or_404

from company.models import Company
from .models import Invoice
from sales_order.models import SalesOrder, SalesOrderProduct
from clients.models import Clients
from random import randint
from django.contrib.auth.decorators import login_required

@login_required
def open_invoice(request, id):
    companies = Company.objects.all()
    sale_order = get_object_or_404(SalesOrder, pk=id)
    sale_order_products = SalesOrderProduct.objects.filter(sale_order=sale_order)
    invoice = Invoice.objects.get(sale_order=sale_order)
    context = {
        "companies": companies,
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