import decimal
from django.shortcuts import render, redirect
from .models import Transaction, Inventory
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
            inventory = Inventory.objects.get(product__id=request.POST.get("product"))
            type = request.POST.get("type")
            quantity = decimal.Decimal(request.POST.get("quantity"))

            if not inventory:
                messages.error(request, "Não foi possível realizar a transação, verifique se o produto está cadastrado no estoque.")
                context = { "form": form}
        
                return render(request, "transactions/create.html", context)

            try:
                with transaction.atomic():
                    if type == "OUT":
                        if inventory.quantity - quantity < 0:
                            transaction_error = TransactionQuantityError("Quantidade indisponível no estoque")
                            print(transaction_error)
                            raise transaction_error
                        else:
                            inventory.quantity -= quantity
                            inventory.save()

                    elif type == "IN":
                        inventory.quantity += quantity
                        print(quantity)
                        print(inventory.quantity)
                        inventory.save()
            except:
                messages.error(request, "Não foi possível realizar a transação.")
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

def inventory_index(request):
    inventory = Inventory.objects.all()

    context = {
        "inventory": inventory
    }

    return render(request, "inventory/index.html", context)

def inventory_search(request):
    search_value = request.GET.get("q").strip()


    if not search_value:
        return redirect("inventory:index")
    
    inventory = Inventory.objects\
        .filter(Q(product__icontains=search_value) | Q(quantity__icontains=search_value))\
        .order_by("-product")
    
    context = {
        "inventory": inventory
    }

    return render(request, "inventory/index.html", context)
