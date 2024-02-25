from django.shortcuts import render
from .models import Product, SupplierProduct, Category
from inventory.models import Inventory
from django.db.models import Q
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .forms import ProductForm, CategoryForm
from .forms import SupplierProductFormSet
from sales_order.models import SalesOrderProduct
from inventory.models import Inventory
from django.db.models import Count
from .filters import ProductFilter
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    products = Product.objects.order_by("-id")
    inventory_quantity = Inventory.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products)
    # Aplicando a paginação
    paginator = Paginator(product_filter.qs, 100)
    # /produtos?page=1 -> Obtendo a página da URL
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "inventory_quantity": inventory_quantity,
        'filter': product_filter
        }
    
    return render(request, "products/index.html", context)

# def search(request):
#     # Obtendo o valor da requisição (Formulário)
#     search_value = request.GET.get("q").strip()

#     # Verificando se algo foi digitado
#     if not search_value:
#         return redirect("products:index")
    
#     # Filtrando os produtos
#     #  O Q é usado para combinar filtros (& ou |)
#     products = Product.objects\
#         .filter(Q(name__icontains=search_value))\
#         .order_by("-id")

#     paginator = Paginator(products, 100)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     context = { "products": page_obj}

#     return render(request, "products/index.html", context)

def create(request):
    form_action = reverse("products:create")
    # POST
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
    product = get_object_or_404(Product, pk=id)

    sales_order_count = SalesOrderProduct.objects.filter(product=product).aggregate(count=Count('id'))['count']
    if sales_order_count > 0:
        messages.error(request, f"Não é possível excluir um produto que está associado a um pedido de vendas.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    transactions_count = Inventory.objects.filter(product=product).aggregate(count=Count('id'))['count']
    if transactions_count > 0:
        messages.error(request, f"Não foi possível excluir o produto, pois o mesmo já possui transações. Considere inativá-lo.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    product.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def toggle_enabled(request, id):
    product = get_object_or_404(Product, pk=id)
    
    pending_sale_order = SalesOrderProduct.objects.filter(product=product, sale_order__status="Pendente").aggregate(count=Count('id'))['count']
    if pending_sale_order > 0:
        messages.error(request, f"Não é possível inativar um produto que contém um pedido de vendas pendente.")
        return JsonResponse({ "message": "error" })
    product.enabled = not product.enabled
    product.save()
    
    return JsonResponse({ "message": "success" })

@require_POST
def delete_supplier_from_product(request, id):
    supplier_product = get_object_or_404(SupplierProduct, pk=id)
    supplier_product.delete()

    return JsonResponse({"message": "success"})

@require_GET
def get_suppliers_from_product(request, id):
    suppliers = SupplierProduct.objects.filter(product__id=id).order_by("-id")

    # Serialização
    suppliers_serialized = [{
        "id": supplierProduct.id,
        "name": supplierProduct.supplier.fantasy_name,
        "cost_price": supplierProduct.cost_price
    } for supplierProduct in suppliers] 

    return JsonResponse(suppliers_serialized, safe=False)

# Categories

class CategoryListView(PermissionRequiredMixin, ListView):
    model = Category
    template_name = "categories/index.html"
    paginate_by = 100
    permission_required = "products.view_category"


def search_categories(request):
    # Obtendo o valor da requisição (Formulário)
    search_value = request.GET.get("q").strip()

    # Verificando se algo foi digitado
    if not search_value:
        return redirect("products:categories")
    
    # Filtrando os produtos
    categories = Category.objects.filter(Q(name__icontains=search_value)).order_by("-id")
    
    # Aplicando a paginação
    paginator = Paginator(categories, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"categories": page_obj}
    return render(request, "categories/index.html", context)

def create_category(request):
    form_action = reverse("products:category_create")

    # POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save() # Salva o produto no banco de dados
            messages.success(request, "A categoria foi cadastrada com sucesso!")
            return redirect("products:categories")
        
        messages.error(request, "Falha ao cadastrar a categoria. Verifique o preenchimento dos campos.")
        context = {"form": form, "form_action": form_action}
        return render(request, "categories/create.html", context)

    # GET
    form = CategoryForm()
    context = {"form": form, "form_action": form_action}
    return render(request, "categories/create.html", context)

def update_category(request, id):
    category = get_object_or_404(Product, id=id)
    form_action = reverse("products:category_update", args=(id,))

    #POST 
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request,"Categoria atualizado com sucesso!")
            return redirect("products:categories")
        else:
            messages.error(request, "Erro ao atualizar a categoria. Verifique os dados informados.")
        
        context = {"form": form, "form_action": form_action}
        return render(request, "categories/create.html", context)
    
    # GET
    form =  ProductForm(instance=category)
    context = {"form": form, "form_action": form_action}
    return render(request, "categories/create.html", context)

@require_POST
def delete_category(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()
    return redirect("products:categories")