from django.shortcuts import get_object_or_404, redirect, render
from django.db import IntegrityError, transaction
from .models import Purchases, PurchasesProduct
from django.http import HttpResponseRedirect, JsonResponse
from products.models import Product
from django.views.generic import ListView
from .forms import PurchasesForm, PurchasesProductFormSet
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from transactions.models import Transaction

class PurchasesListView(ListView):
    model = Purchases
    template_name = "purchases/index.html"
    paginate_by = 10
    ordering = "-id"
    
def create(request):
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
                messages.success(request, "O produto foi cadastrado com sucesso!")
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

def get_sale_value(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'GET':
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id=product_id)
        sale_price = product.sale_price
        return JsonResponse({'sale_price': sale_price})
    else:
        return JsonResponse({'error': 'Invalid request'})    

def get_sale_value_update(request, id):
    value = get_sale_value(request)
    return value

def get_sale_value_create(request):
    value = get_sale_value(request)
    return value

def update(request, id):
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

def finish_order(request, id):
    purchase = get_object_or_404(Purchases, pk=id)
    print(PurchasesProduct.objects.all())
    for purchase_product in PurchasesProduct.objects.filter(purchase=purchase):
            try:
                Transaction.create(product=purchase_product.product, quantity=purchase_product.amount, type="IN")
            except:
                messages.error(request, "Não foi possível faturar o pedido, verifique o estoque")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    with transaction.atomic():
        try:
            purchase.status = "Confirmado"
            purchase.save()
            messages.success(request, "Pedido faturado com sucesso!")
        except:
            purchase.status = "Pendente"
            messages.error(request, "Não foi possível faturar o pedido.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def cancel(request, id):
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
    supplier_product = get_object_or_404(PurchasesProduct, pk=id)
    supplier_product.delete()

    return JsonResponse({ "message": "success"})

@require_GET
def get_products_from_purchase(request, id):
    products = PurchasesProduct.objects.filter(sale_order__id=id).order_by("-id")

    # Serialização
    products_serialized = [{
        "name": PurchasesProduct.product.name,
        "unit_of_measurement": PurchasesProduct.product.unit_of_measurement,
        "amount": PurchasesProduct.amount,
        "total_value": PurchasesProduct.total_value_product,
    } for PurchasesProduct in products]

    return JsonResponse(products_serialized, safe = False)

def finish_order(request, id):
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