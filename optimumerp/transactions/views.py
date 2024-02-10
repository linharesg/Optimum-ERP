from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionsForm
from django.core.paginator import Paginator
from django.contrib import messages

def index(request):
    transactions = Transaction.objects.order_by("-id")

    paginator = Paginator(transactions, 100)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "transactions": page_obj
    }
    
    return render(request, "transactions/index.html", context)

def create(request):
    if request.method == 'POST':
        form = TransactionsForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Produto cadastrado com sucesso!")
            
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
    ...
    