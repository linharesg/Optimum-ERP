from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from .models import SalesOrder
from django.views.generic import ListView, CreateView
from .forms import SalesOrderForm, SalesOrderProductFormSet
from django.contrib import messages
from products.models import Product

# Create your views here.

class SalesOrderListView(ListView):
    model = SalesOrder
    template_name = "sales_order/index.html"
    paginate_by = 1
    ordering = "-id"


def create(request):
    # POST
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)

        if form.is_valid():
            sale_order = form.save(commit=False)
            sale_order_product_formset = SalesOrderProductFormSet(request.POST, instance=sale_order)
            
            if not sale_order_product_formset.is_valid():                      
                messages.error(request, "Falha ao cadastrar os produtos do pedido de venda")
                
                sale_order_product_formset = SalesOrderProductFormSet(request.POST)

                context = { 
                    "form": form, 
                    "sale_order_product_formset": sale_order_product_formset, 
                    }
                
                return render(request, "sales_order/create.html", context)

            if sale_order_product_formset.is_valid():
                messages.success(request, "O produto foi cadastrado com sucesso!")
                form.save()
                sale_order_product_formset.save()
                return redirect("sales_order:index")
            else:
    
                messages.error(request, "Falha ao cadastrar o estoque do produto")
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
    print("oioi")
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'GET':
        print("teste")
        product_id = request.GET.get('product_id')
        print(product_id)
        product = Product.objects.get(id=product_id)
        sale_price = product.sale_price
        return JsonResponse({'sale_price': sale_price})
    else:
        print("af")
        return
        return JsonResponse({'error': 'Invalid request'})