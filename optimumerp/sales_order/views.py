from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from .models import SalesOrder
from django.views.generic import ListView, CreateView
from .forms import SalesOrderForm, SalesOrderProductFormSet
from django.contrib import messages

# Create your views here.

class SalesOrderListView(ListView):
    model = SalesOrder
    template_name = "sales_order/index.html"
    paginate_by = 1
    ordering = "-id"

# class SalesOrderCreateView(CreateView):
#     model = SalesOrder
#     template_name = "sales_order/create.html"
#     form_class = SalesOrderForm
#     success_url = reverse_lazy("suppliers:index")
    
def create(request):
    form_action = reverse("sales_order:create")
    # POST
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)
        print("linha 27")

        if form.is_valid():

                print("linha29")

                sale_order = form.save()
                
                sale_order_product_formset = SalesOrderProductFormSet(request.POST, instance=sale_order)
                
                if not sale_order_product_formset.is_valid():                      
                    messages.error(request, "Falha ao cadastrar os produtos do pedido de venda")
                    sale_order.delete()
                    
                    sale_order_product_formset = SalesOrderProductFormSet(request.POST)

                    context = { 
                        "form": form, 
                        "sale_order_product_formset": sale_order_product_formset, 
                        "form_action": form_action,
                        }
                    
                    return render(request, "sales_order/create.html", context)
                
                return redirect("sales_order:index")

    # GET
    form = SalesOrderForm(initial={'status': "Pendente"})
    # form = SalesOrderForm()
    sale_order_product_formset = SalesOrderProductFormSet()
    
    context = {
        "form": form, 
        "form_action": form_action,
        "sale_order_product_formset": sale_order_product_formset,
        }

    return render(request, "sales_order/create.html", context)