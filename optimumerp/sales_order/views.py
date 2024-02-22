from django import forms
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from .models import SalesOrder, SalesOrderProduct
from django.views.generic import ListView, CreateView
from .forms import SalesOrderForm, SalesOrderProductFormSet
from django.contrib import messages
from products.models import Product
from transactions.models import Transaction
from django.views.decorators.http import require_POST, require_GET

# Create your views here.

class SalesOrderListView(ListView):
    model = SalesOrder
    template_name = "sales_order/index.html"
    paginate_by = 10
    ordering = "-id"


def create(request):
    # POST
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)

        if form.is_valid():
            sale_order = form.save(commit=False)
            sale_order_product_formset = SalesOrderProductFormSet(request.POST, instance=sale_order)
            
            if not sale_order_product_formset.is_valid():                      
                messages.error(request, "Falha ao cadastrar os produtos do pedido de venda.")
                
                sale_order_product_formset = SalesOrderProductFormSet(request.POST)

                context = { 
                    "form": form, 
                    "sale_order_product_formset": sale_order_product_formset, 
                    }
                
                return render(request, "sales_order/create.html", context)

            if sale_order_product_formset.is_valid():
                messages.success(request, "O pedido de venda foi emitido com sucesso!")
                sale_order.user = request.user
                sale_order.save()
                sale_order_product_formset.save()
                return redirect("sales_order:index")
            else:
    
                messages.error(request, "Falha ao cadastrar o pedido.")
                sale_order.delete()
                sale_order_product_formset = sale_order_product_formset(request.POST)

                context = { 
                    "form": form, 
                    "sale_order_product_formset": sale_order_product_formset, 
                    }
                
                return render(request, "sales_order/create.html", context)

        else:
            sale_order_product_formset = SalesOrderProductFormSet()
            context = { 
            "form": form, 
            "sale_order_product_formset": sale_order_product_formset, 
            }
        
            return render(request, "sales_order/create.html", context)
    
    # GET
    form = SalesOrderForm(initial={'status': "Pendente"})
    sale_order_product_formset = SalesOrderProductFormSet()
    
    context = {
        "form": form, 
        "sale_order_product_formset": sale_order_product_formset,
        }

    return render(request, "sales_order/create.html", context)

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

    sale_order = get_object_or_404(SalesOrder, pk=id)

    if sale_order.status == "Cancelado":
        messages.error(request, f"Erro ao editar o pedido {sale_order.id}: Não é possível editar um pedido cancelado.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    if sale_order.status == "Confirmado":
        messages.error(request, f"Erro ao cancelar pedido {sale_order.id}: Não é possível editar um pedido que já foi confirmado.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == "POST":
        form = SalesOrderForm(request.POST, instance=sale_order)
        form.fields['client'].widget.attrs['readonly'] = 'readonly'
        sale_order_product_formset = SalesOrderProductFormSet(
            request.POST, instance=sale_order)

        if form.is_valid():
            try:
                form.save()

                if sale_order_product_formset.is_valid():
                    sale_order_product_formset.save()
                    messages.success(request, "Pedido atualizado com sucesso!")
                    return redirect("sales_order:index")
                else:
                    messages.error(
                        request, "Falha ao atualizar o pedido. Verifique os produtos do pedido.")

            except IntegrityError:
                messages.error(
                    request, "Falha ao atualizar o pedido: Não é possível ter o mesmo produto mais de uma vez em um único produto.")
        else:
            messages.error(
                request, "Falha ao atualizar o pedido: formulário inválido.")
        
        
        sale_order_product_formset = SalesOrderProductFormSet(instance=sale_order)
        context = {
            "form": form,
            "sale_order_product_formset": sale_order_product_formset
        }
        
        return render(request, "sales_order/update.html", context)

      
    form = SalesOrderForm(instance=sale_order)
    form.fields['client'].widget.attrs['readonly'] = 'readonly'
    form.fields['user'].widget.attrs['readonly'] = 'readonly'
    sale_order_product_formset = SalesOrderProductFormSet(instance=sale_order)

    context = {
        "form": form,
        "sale_order_product_formset": sale_order_product_formset
    }

    return render(request, "sales_order/update.html", context)

def finish_order(request, id):
    sale_order = get_object_or_404(SalesOrder, pk=id)
    for sale_products in SalesOrderProduct.objects.filter(sale_order=sale_order):
        try:
            Transaction.create(product=sale_products.product, quantity=sale_products.amount, type="OUT")
        except:
            messages.error(request, "Não foi possível faturar o pedido, verifique o estoque")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    with transaction.atomic():
        try:
            sale_order.status = "Confirmado"
            sale_order.save()
            messages.success(request, "Pedido faturado com sucesso!")
        except:
            messages.error(request, "Não foi possível faturar o pedido.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    


@require_POST
def cancel(request, id):
    sale_order = get_object_or_404(SalesOrder, pk=id)

    if sale_order.status == "Cancelado":
        messages.error(request, f"Erro ao cancelar pedido: o pedido {sale_order.id} já está cancelado!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if sale_order.status == "Confirmado":
        messages.error(request, f"Erro ao cancelar pedido {sale_order.id}: Você não pode cancelar um pedido que já foi confirmado!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    if sale_order.status == "Pendente":
        sale_order.status = "Cancelado"
        sale_order.save()
        messages.success(request, f"O pedido {sale_order.id} foi cancelado.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def delete_product_from_sale_order(request, id):
    supplier_product = get_object_or_404(SalesOrderProduct, pk=id)
    supplier_product.delete()

    return JsonResponse({ "message": "success"})

@require_GET
def get_products_from_sale_order(request, id):
    products = SalesOrderProduct.objects.filter(sale_order__id=id).order_by("-id")

    # Serialização
    products_serialized = [{
        "name": SalesOrderProduct.product.name,
        "unit_of_measurement": SalesOrderProduct.product.unit_of_measurement,
        "amount": SalesOrderProduct.amount,
        "total_value": SalesOrderProduct.total_value_product,
    } for SalesOrderProduct in products]

    return JsonResponse(products_serialized, safe = False)

