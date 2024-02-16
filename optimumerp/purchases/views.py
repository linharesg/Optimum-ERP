from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from .models import Purchases
from django.views.generic import ListView, CreateView
from .forms import PurchasesForm, PurchasesProductFormSet
from django.contrib import messages

# Create your views here.

class PurchasesListView(ListView):
    model = Purchases
    template_name = "purchases/index.html"
    paginate_by = 1
    ordering = "-id"

class PurchasesCreateView(CreateView):
    model = Purchases
    template_name = "purchases/create.html"
    form_class = PurchasesForm
    success_url = reverse_lazy("suppliers:index")
    
def create(request):
    form_action = reverse("purchases:create")
    # POST
    if request.method == 'POST':
        form = PurchasesForm(request.POST)
        print("linha 27")

        if form.is_valid():
            print("linha29")
            purchase = form.save()
            
            purchase_product_formset = PurchasesProductFormSet(request.POST, instance=purchase)

            if not purchase_product_formset.is_valid():                      
                messages.error(request, "Falha ao cadastrar os produtos do pedido de venda")
                purchase.delete()
                
                purchase_product_formset = PurchasesProductFormSet(request.POST)

                context = { 
                    "form": form, 
                    "purchase_product_formset": purchase_product_formset, 
                    "form_action": form_action,
                    }
                
                return render(request, "purchases/create.html", context)

            if purchase_product_formset.is_valid():
                messages.success(request, "O produto foi cadastrado com sucesso!")
                purchase_product_formset.save()

            else:
                messages.error(request, "Falha ao cadastrar o estoque do produto")
                purchase.delete()
                purchase_product_formset = purchase_product_formset(request.POST)

                context = { 
                    "form": form, 
                    "purchase_product_formset": purchase_product_formset, 
                    }
                
                return render(request, "purchases/create.html", context)
            
            return redirect("purchases:index")

    # GET
    form = PurchasesForm(initial={'status': "Pendente"})
    # form = PurchasesForm()
    purchase_product_formset = PurchasesProductFormSet()
    
    context = {
        "form": form, 
        "form_action": form_action,
        "purchase_product_formset": purchase_product_formset,
        }

    return render(request, "purchases/create.html", context)