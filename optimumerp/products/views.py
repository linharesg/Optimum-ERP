from django.shortcuts import render
from .models import Product, SupplierProduct
from inventory.models import Inventory
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .forms import ProductForm
from .forms import SupplierProductFormSet
from sales_order.models import SalesOrderProduct
from inventory.models import Inventory
from django.db.models import Count
from .filters import ProductFilter
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """

    Esta função exibe uma lista paginada de todos os produtos no sistema, permitindo a filtragem por meio de parâmetros de consulta.
    
    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.

    Returns:
        HttpResponse: Uma resposta HTTP que renderiza a página de listagem de produtos.
    """    
    # Obtendo todos os produtos e a quantidade em estoque
    products = Product.objects.order_by("-id")
    inventory_quantity = Inventory.objects.all()

    # Aplicando filtros de pesquisa
    product_filter = ProductFilter(request.GET, queryset=products)

    # Aplicando a paginação
    paginator = Paginator(product_filter.qs, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "inventory_quantity": inventory_quantity,
        'filter': product_filter
        }
    
    return render(request, "products/index.html", context)

def create(request):
    """

    Esta função exibe o formulário de criação de um novo produto e processa a submissão do formulário. 
    Após a submissão bem-sucedida do formulário, o produto é salvo no banco de dados e um registro é criado na tabela Inventory.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.

    Returns:
        HttpResponse: Uma resposta HTTP que renderiza a página de criação de produtos ou redireciona para a página de listagem de produtos após a criação bem-sucedida.
    """    
    form_action = reverse("products:create")

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
                product = form.save() # Salva o produto no banco de dados
                try:
                    Inventory.objects.create(product=product, quantity=0) # Cria um registro na tabela Inventory
                except:
                    messages.error(request, "Falha ao cadastrar o produto no estoque")
                    product.delete() # Deleta o produto caso não crie o registro na tabela Inventory

                    context = { 
                        "form": form, 
                        "supplier_product_formset": supplier_product_formset, 
                        "form_action": form_action,
                        }
                    
                    return render(request, "products/create.html", context)
                
                supplier_product_formset = SupplierProductFormSet(request.POST, instance=product)
                
                if not supplier_product_formset.is_valid():     
                    # Se o formulário de fornecedores não for válido, exclui o produto                 
                    messages.error(request, "Falha ao cadastrar os fornecedores do produto")
                    product.delete()
                    
                    supplier_product_formset = SupplierProductFormSet(request.POST)
            
                    context = { 
                        "form": form, 
                        "supplier_product_formset": supplier_product_formset, 
                        "form_action": form_action,
                        }
                    
                    return render(request, "products/create.html", context)
                
                supplier_product_formset.save()

                return redirect("products:index")

    # GET
    form = ProductForm()
    supplier_product_formset = SupplierProductFormSet()

    context = {
        "form": form, 
        "form_action": form_action,
        "supplier_product_formset": supplier_product_formset
        }

    return render(request, "products/create.html", context)

def update(request, slug):
    """
    Esta função exibe o formulário de atualização de um produto existente e processa a submissão do formulário. 
    Após a submissão bem-sucedida do formulário, o produto é atualizado no banco de dados.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        slug (str): O slug único do produto a ser atualizado.

    Returns:
        HttpResponse: Uma resposta HTTP que renderiza o formulário de atualização de produto ou redireciona para a página de listagem de produtos após a atualização bem-sucedida.
    """    
    product = get_object_or_404(Product, slug=slug)
    form_action = reverse("products:update", args=(slug,))

    # POST
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        supplier_product_formset = SupplierProductFormSet(request.POST, instance=product)
        
        if form.is_valid():
            if supplier_product_formset.is_valid():
                try:
                    supplier_product_formset.save()
                    messages.success(request, "Produto atualizado com sucesso!")

                except IntegrityError:
                    messages.error(request, "Existem fornecedores duplicados.")
                    context = {
                        "form_action": form_action,
                        "supplier_product_formset": supplier_product_formset,
                        "form": form
                    }

                    return render(request, "products/create.html", context)
            
            form.save()
            print(supplier_product_formset)
            # messages.success(request, "Produto atualizado com sucesso!")
            return redirect("products:index")
        
        messages.error(request, "Não foi possível atualizar o produto.")
        context = {
            "form_action": form_action,
            "form": form
        }

        return render(request, "products/create.html", context)
    
    # GET
    form =  ProductForm(instance=product)
    supplier_product_formset = SupplierProductFormSet(instance=product)
    context = {
        "form_action": form_action,
        "form": form,
        "supplier_product_formset": supplier_product_formset,
    }

    return render(request, "products/create.html", context)

@require_POST
def delete(request, id):
    """
    Esta função exclui um produto do banco de dados se não estiver associado a nenhum pedido de venda ou transação de estoque.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        id (int): O ID do produto a ser excluído.

    Returns:
        HttpResponseRedirect: Redireciona o usuário de volta à página anterior após a exclusão bem-sucedida do produto.
    """    
    product = get_object_or_404(Product, pk=id)

    # Verifica se o produto está associado a pedidos de vendas pendentes
    sales_order_count = SalesOrderProduct.objects.filter(product=product).aggregate(count=Count('id'))['count']
    if sales_order_count > 0:
        messages.error(request, f"Não é possível excluir um produto que está associado a um pedido de vendas.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # Verifica se o produto está associado a transações de estoque
    transactions_count = Inventory.objects.filter(product=product).aggregate(count=Count('id'))['count']
    if transactions_count > 0:
        messages.error(request, f"Não foi possível excluir o produto, pois o mesmo já possui transações. Considere inativá-lo.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    # Exclui o produto do banco de dados    
    product.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def toggle_enabled(request, id):
    """
    Esta função alterna o status de ativação de um produto entre ativo e inativo.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        id (int): O ID do produto a ter o status de ativação alterado.

    Returns:
        JsonResponse: Retorna uma resposta JSON indicando o sucesso da operação.
    """    
    product = get_object_or_404(Product, pk=id)

    # Verifica se o produto está associado a pedidos de vendas pendentes
    pending_sale_order = SalesOrderProduct.objects.filter(product=product, sale_order__status="Pendente").aggregate(count=Count('id'))['count']
    if pending_sale_order > 0:
        messages.error(request, f"Não é possível inativar um produto que contém um pedido de vendas pendente.")
        return JsonResponse({ "message": "error" })
    
    # Alterna o status de ativação do produto
    product.enabled = not product.enabled
    product.save()
    
    return JsonResponse({ "message": "success" })

@require_POST
def delete_supplier_from_product(request, id):
    """
    Esta função exclui um registro de fornecedor associado a um produto do banco de dados.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        id (int): O ID do registro do fornecedor a ser excluído.

    Returns:
        JsonResponse: Retorna uma resposta JSON indicando o sucesso da operação.
    """
    supplier_product = get_object_or_404(SupplierProduct, pk=id)
    supplier_product.delete()

    return JsonResponse({"message": "success"})

@require_GET
def get_suppliers_from_product(request, id):
    """
    Esta função retorna uma lista de fornecedores associados a um produto em formato JSON.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        id (int): O ID do produto.

    Returns:
        JsonResponse: Retorna uma resposta JSON contendo a lista de fornecedores associados ao produto.
    """
    suppliers = SupplierProduct.objects.filter(product__id=id).order_by("-id")

    # Serializa os dados dos fornecedores
    suppliers_serialized = [{
        "id": supplierProduct.id,
        "name": supplierProduct.supplier.fantasy_name,
        "cost_price": supplierProduct.cost_price
    } for supplierProduct in suppliers] 

    return JsonResponse(suppliers_serialized, safe=False)
