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
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """
    Esta view é responsável por exibir a página inicial do módulo de transações, listando todas as transações registradas
    no sistema. Também fornece filtros para pesquisar transações específicas.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.

    Returns:
        HttpResponse: Uma resposta HTTP que renderiza a página inicial do módulo de transações.

    """
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
    """
    Esta view é responsável por criar uma nova transação com base nos dados fornecidos pelo usuário. 
    Os dados são enviados através de um formulário POST. Antes de salvar a transação, verifica-se 
    se a quantidade da transação é válida em relação ao estoque disponível.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.

    Returns:
        HttpResponse: Uma resposta HTTP que renderiza o formulário de criação de transação ou redireciona para a página inicial do módulo de transações após a criação bem-sucedida.

    """
    if request.method == 'POST':
        form = TransactionsForm(request.POST)
        inventory = Inventory.objects.get(product=request.POST.get("product"))
        quantity = decimal.Decimal(request.POST.get("quantity"))
        if form.is_valid():
            try:
                form.save()
                if request.POST.get("type") == "IN":
                    inventory.quantity += quantity
                    inventory.save()
                else:
                    if inventory.quantity - quantity < 0:
                        raise TransactionQuantityError("Quantidade indisponível no estoque")
                    else:
                        inventory.quantity -= quantity
                        inventory.save()
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