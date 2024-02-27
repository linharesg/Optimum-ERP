from django.shortcuts import get_object_or_404, redirect, render
from django.db import IntegrityError, transaction
from .models import Purchases, PurchasesProduct
from django.http import HttpResponseRedirect, JsonResponse
from products.models import Product, SupplierProduct
from .forms import PurchasesForm, PurchasesProductFormSet
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from transactions.models import Transaction
from .filters import PurchasesFilter
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """
    Esta função exibe uma lista paginada de todos os pedidos de compra no sistema, permitindo a filtragem e pesquisa.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.

    Returns:
        HttpResponse: Uma resposta HTTP que renderiza a página de listagem de pedidos de compra.
    """
    purchase = Purchases.objects.order_by("-id")
    purchase_filter = PurchasesFilter(request.GET, queryset=purchase)
    paginator = Paginator(purchase_filter.qs.distinct(), 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "filter": purchase_filter
    }

    return render(request, "purchases/index.html", context)

def create(request):
    """
    Esta função cria um novo pedido de compra no sistema, permitindo a inclusão de produtos associados.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.

    Returns:
        HttpResponse: Uma resposta HTTP que renderiza a página de criação de pedidos de compra.
    """
    # POST
    if request.method == 'POST':
        form = PurchasesForm(request.POST)

        if form.is_valid():
            purchase = form.save(commit=False)            
            purchase_product_formset = PurchasesProductFormSet(request.POST, instance=purchase)

            if not purchase_product_formset.is_valid():                      
                messages.error(request, "Falha ao cadastrar os produtos do pedido de compra.")
                
                purchase_product_formset = PurchasesProductFormSet(request.POST)
                
                context = { 
                    "form": form, 
                    "purchase_product_formset": purchase_product_formset, 
                }

                return render(request, "purchases/create.html", context)

            if purchase_product_formset.is_valid():
                messages.success(request, "O pedido de compra foi cadastrado com sucesso!")
                purchase.user = request.user
                purchase.save()
                purchase_product_formset.save()
                return redirect("purchases:index")
            
            else:
                messages.error(request, "Falha ao cadastrar o pedido.")
                purchase.delete()
                purchase_product_formset = purchase_product_formset(request.POST)

                context = { 
                    "form": form, 
                    "purchase_product_formset": purchase_product_formset, 
                    }
                
                return render(request, "purchases/create.html", context)
            
        else:
            purchase_product_formset = PurchasesProductFormSet()
            
            context = { 
            "form": form, 
            "purchase_product_formset": purchase_product_formset, 
            }
        
            return render(request, "purchases/create.html", context)    
            
    form = PurchasesForm(initial={'status': "Pendente"})
    purchase_product_formset = PurchasesProductFormSet()

    context = {
        "form": form, 
        "purchase_product_formset": purchase_product_formset,
        }

    return render(request, "purchases/create.html", context)