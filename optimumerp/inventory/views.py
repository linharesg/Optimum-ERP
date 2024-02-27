from django.shortcuts import render, redirect
from .models import Inventory
from .filters import InventoryFilter
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """
    Esta view requer que o usuário esteja autenticado. Ela recupera todos os objetos do modelo Inventory
    e os filtra de acordo com os parâmetros fornecidos na requisição GET. Os resultados são então paginados
    e enviados para o template "inventory/index.html" para exibição.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada contendo a lista paginada de itens de inventário.
    """
    inventory = Inventory.objects.all()
    inventory_filter = InventoryFilter(request.GET, queryset=inventory)
    
    paginator = Paginator(inventory_filter.qs, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        'filter': inventory_filter
    }

    return render(request, "inventory/index.html", context)
