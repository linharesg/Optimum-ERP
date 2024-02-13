from django.shortcuts import render
from .models import SalesOrder
# Create your views here.

def index(request):
    orders = SalesOrder.objects.order_by("-id")

    context = {
        "orders": orders
    }
    
    return render(request, "sales_order/index.html", context)
