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

    # Aplicando a paginação
    purchase = Purchases.objects.order_by("-id")
    purchase_filter = PurchasesFilter(request.GET, queryset=purchase)
    paginator = Paginator(purchase_filter.qs.distinct(), 50)

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

def get_purchasing_price(request):
    """
    Esta função é acionada via requisição AJAX e retorna o preço de compra de um produto de um fornecedor específico.
    Ela espera receber o ID do produto e o ID do fornecedor como parâmetros na consulta GET.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.

    Returns:
        JsonResponse: Uma resposta JSON contendo o preço de compra do produto. Se a requisição não for uma solicitação AJAX ou se os parâmetros estiverem ausentes, uma mensagem de erro é retornada.
    """
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'GET':
        product_id = request.GET.get('product_id')
        supplier_id = request.GET.get('supplier')

        product = SupplierProduct.objects.filter(product_id=product_id, supplier_id=supplier_id).first()
        purchasing = ""
        if product:
            purchasing = product.cost_price
        return JsonResponse({'purchasing': purchasing})
    else:
        return JsonResponse({'error': 'Invalid request'})    

def get_purchasing_price_update(request, id):
    """
    Esta função é usada para retornar o preço de compra de um produto quando o usuário está atualizando um pedido de compra.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        id (int): O ID do pedido de compra.

    Returns:
        JsonResponse: Uma resposta JSON contendo o preço de compra do produto.
    """
    value = get_purchasing_price(request)
    return value

def get_purchasing_price_create(request):
    """
    Esta função é usada para retornar o preço de compra de um produto quando o usuário está criando um novo pedido de compra.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.

    Returns:
        JsonResponse: Uma resposta JSON contendo o preço de compra do produto.
    """
    value = get_purchasing_price(request)
    return value

def update(request, id):
    """
    Esta função é responsável por atualizar um pedido de compra existente com base nos dados fornecidos pelo usuário.
    Os dados são enviados através de um formulário POST. Se a atualização for bem-sucedida, o usuário é redirecionado para a página de listagem de pedidos de compra.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        id (int): O ID do pedido de compra a ser atualizado.

    Returns:
        HttpResponse: Uma resposta HTTP que redireciona o usuário para a página de listagem de pedidos de compra após a atualização.
    """
    purchase = get_object_or_404(Purchases, pk=id)

    if purchase.status == "Cancelado":
        messages.error(request, f"Erro ao editar o pedido {purchase.id}: Não é possível editar um pedido cancelado.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if purchase.status == "Confirmado":
        messages.error(request, f"Erro ao cancelar pedido {purchase.id}: Não é possível editar um pedido que já foi confirmado.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == "POST":
        form = PurchasesForm(request.POST, instance=purchase)
        form.fields['supplier'].widget.attrs['readonly'] = 'readonly'
        purchase_product_formset = PurchasesProductFormSet(request.POST, instance=purchase)

        if form.is_valid():
            try:
                form.save()
                if purchase_product_formset.is_valid():
                    purchase_product_formset.save()
                    messages.success(request, "Pedido atualizado com sucesso!")
                    return redirect("purchases:index")
                else:
                    messages.error(request, "Falha ao atualizar o pedido. Verifique os produtos do pedido.")
            except IntegrityError:
                messages.error(request, "Falha ao atualizar o pedido: Não é possível ter o mesmo produto mais de uma vez em um único pedido.")
        else:
            messages.error(request, "Falha ao atualizar o pedido: formulário inválido.")

        purchase_product_formset = PurchasesProductFormSet(instance=purchase)

        context = {
            "form": form,
            "purchase_product_formset": purchase_product_formset
        }

        return render(request, "purchases/update.html", context)

    form = PurchasesForm(instance=purchase)
    form.fields['supplier'].widget.attrs['readonly'] = 'readonly'
    form.fields['user'].widget.attrs['readonly'] = 'readonly'
    purchase_product_formset = PurchasesProductFormSet(instance=purchase)

    context = {
        "form": form,
        "purchase_product_formset": purchase_product_formset
    }

    return render(request, "purchases/update.html", context)

@require_POST
def cancel(request, id):
    """
    Esta função é responsável por cancelar um pedido de compra existente. Se o pedido estiver no estado "Pendente", ele será cancelado com sucesso e uma mensagem de sucesso será exibida. Caso contrário, uma mensagem de erro informando que o pedido não pode ser cancelado será exibida.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        id (int): O ID do pedido de compra a ser cancelado.

    Returns:
        HttpResponse: Uma resposta HTTP que redireciona o usuário de volta à página anterior após o cancelamento do pedido.
    """
    purchase = get_object_or_404(Purchases, pk=id)

    if purchase.status == "Cancelado":
        messages.error(request, f"Erro ao cancelar pedido: o pedido {purchase.id} já está cancelado!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if purchase.status == "Confirmado":
        messages.error(request, f"Erro ao cancelar pedido {purchase.id}: Você não pode cancelar um pedido que já foi confirmado!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if purchase.status == "Pendente":
        purchase.status = "Cancelado"
        purchase.save()
        messages.success(request, f"O pedido {purchase.id} foi cancelado.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def delete_product_from_purchase(request, id):
    """
    Esta função é responsável por excluir um produto de um pedido de compra existente com base no ID do produto.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        id (int): O ID do produto a ser excluído do pedido de compra.

    Returns:
        JsonResponse: Uma resposta JSON indicando o sucesso da exclusão do produto.
    """
    supplier_product = get_object_or_404(PurchasesProduct)
    supplier_product.delete()

    return JsonResponse({ "message": "success"})

@require_GET
def get_products_from_purchase(request, id):
    """
    Esta função retorna os detalhes dos produtos associados a um pedido de compra específico em formato JSON.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        id (int): O ID do pedido de compra.

    Returns:
        JsonResponse: Uma resposta JSON contendo os detalhes dos produtos associados ao pedido de compra.
    """
    products = PurchasesProduct.objects.filter(purchase__id=id).order_by("-id")

    # Serialização
    products_serialized = [{
        "name": PurchasesProduct.product.name,
        "unit_of_measurement": PurchasesProduct.product.unit_of_measurement,
        "amount": PurchasesProduct.amount,
        "total_value": PurchasesProduct.total_value_product,
    } for PurchasesProduct in products]

    return JsonResponse(products_serialized, safe=False)

def finish_order(request, id):
    """
    Esta função é responsável por finalizar um pedido de compra, atualizando seu status para "Confirmado" e registrando as transações no estoque correspondente.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        id (int): O ID do pedido de compra a ser finalizado.

    Returns:
        HttpResponse: Uma resposta HTTP que redireciona o usuário de volta à página anterior após o processamento.
    """
    purchase = get_object_or_404(Purchases, pk=id)
    for purchase_product in PurchasesProduct.objects.filter(purchase=purchase):
        try:
            Transaction.create(product=purchase_product.product, quantity=purchase_product.amount, type="IN")
        except:
            messages.error(request, "Não foi possível receber o pedido")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    with transaction.atomic():
        try:
            purchase.status = "Confirmado"
            purchase.save()
            messages.success(request, "Pedido recebido com sucesso!")
        except:
            messages.error(request, "Não foi possível receber o pedido.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))