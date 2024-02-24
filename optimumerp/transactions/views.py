import decimal
from django.shortcuts import render, redirect
from .models import Transaction
from inventory.models import Inventory
from products.models import Product
from .forms import TransactionsForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from .exceptions import TransactionQuantityError
from .filters import TransactionsFilter

def index(request):
    transactions = Transaction.objects.order_by("-id")
    transactions_filter = TransactionsFilter(request.GET, queryset=transactions)

    paginator = Paginator(transactions_filter.qs, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter': transactions_filter
    }
    
    return render(request, "transactions/index.html", context)

def create(request):
    if request.method == 'POST':
        form = TransactionsForm(request.POST)
        product = Product.objects.get(id=request.POST.get("product"))
        if form.is_valid():
            try:
                Transaction.create(product=product, quantity=decimal.Decimal(request.POST.get("quantity")), type=request.POST.get("type"))
            except TransactionQuantityError:
                messages.error(request, "Não foi possível realizar a transação, quantidade insuficiente no estoque.")
                context = { "form": form}
    
                return render(request, "transactions/create.html", context)

            messages.success(request, "Transação cadastrada com sucesso!")
            
            return redirect("transactions:index")
                
        messages.error(request, "Falha ao cadastrar a transação. Verifique o preenchimento dos campos.")
        context = { "form": form}
        
        return render(request, "transactions/create.html", context)

    # GET
    form = TransactionsForm()

    context = {
        "form": form, 
        }

    return render(request, "transactions/create.html", context)

# def search(request):
#     search_value = request.GET.get("q").strip()

#     if not search_value:
#         return redirect("transactions:index")
    
#     transactions = Transaction.objects.filter(Q(product__icontains=search_value) | Q(quantity__icontains=search_value)).order_by("-id")

#     paginator = Paginator(transactions, 2)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     context = {
#         "transactions": page_obj
#     }
    
#     return render(request, "transactions/index.html", context)
