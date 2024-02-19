import decimal
from django.shortcuts import render, redirect
from .models import Transaction
from inventory.models import Inventory
from .forms import TransactionsForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from .exceptions import TransactionQuantityError

def index(request):
    transactions = Transaction.objects.order_by("-id")
    paginator = Paginator(transactions, 2)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "transactions": page_obj,
    }
    
    return render(request, "transactions/index.html", context)

def create(request):
    if request.method == 'POST':
        form = TransactionsForm(request.POST)
        if form.is_valid():
            try:
                Transaction.create(product=request.POST.get("product"), quantity=decimal.Decimal(request.POST.get("quantity")), type=request.POST.get("type"))
            except TransactionQuantityError:
                messages.error(request, "Não foi possível realizar a transação, quantidade insuficiente no estoque.")
                context = { "form": form}
    
                return render(request, "transactions/create.html", context)

            form.save()
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

def search(request):
    search_value = request.GET.get("q").strip()

    if not search_value:
        return redirect("transactions:index")
    
    transactions = Transaction.objects.filter(Q(product__icontains=search_value) | Q(quantity__icontains=search_value)).order_by("-id")

    paginator = Paginator(transactions, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "transactions": page_obj
    }
    
    return render(request, "transactions/index.html", context)
