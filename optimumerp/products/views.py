from django.shortcuts import render
from .models import Product, SupplierProduct
from transactions.models import Inventory
from django.db.models import Q, Sum, F
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from .forms import ProductForm
from .forms import SupplierProductFormSet

# Create your views here.
def index(request):
    products = Product.objects.order_by("-id")
    inventory_quantity = Inventory.objects.all()

    # Aplicando a paginação
    paginator = Paginator(products, 100)
    # /produtos?page=1 -> Obtendo a página da URL
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "inventory_quantity": inventory_quantity
        }
    
    return render(request, "products/index.html", context)

def search(request):
    # Obtendo o valor da requisição (Formulário)
    search_value = request.GET.get("q").strip()

    # Verificando se algo foi digitado
    if not search_value:
        return redirect("products:index")
    
    # Filtrando os produtos
    #  O Q é usado para combinar filtros (& ou |)
    products = Product.objects\
        .filter(Q(name__icontains=search_value))\
        .order_by("-id")

    paginator = Paginator(products, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = { "products": page_obj}

    return render(request, "products/index.html", context)

def create(request):
    form_action = reverse("products:create")
    # POST
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
                product = form.save()
                
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
        if form.is_valid():
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect("products:index")
        
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
    product.delete()

    return redirect("products:index")

@require_POST
def toggle_enabled(request, id):
    product = get_object_or_404(Product, pk=id)

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