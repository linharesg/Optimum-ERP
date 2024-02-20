import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from .forms import SuppliersForm
from .models import Suppliers
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import UpdateView

def index(request):
    suppliers = Suppliers.objects.order_by("-id")

    paginator = Paginator(suppliers, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj
    }
    
    return render(request, "suppliers/index.html", context)

class SupplierUpdateView(UpdateView):
    model = Suppliers
    template_name = "suppliers/update.html"
    form_class = SuppliersForm
    success_url = reverse_lazy("suppliers:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Fornecedor atualizado com sucesso!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.success(self.request, "Erro ao atualizar o fornecedor!")
        return response


def clean_cnpj(value):
    cnpj = re.sub("[^0-9]", "", value)
    return cnpj

def search(request):
    # search_value = request.GET.get("q")
    fantasy_company_name = request.GET.get("fantasy-company-name", "").strip()
    email = request.GET.get("email", "").strip()
    address = request.GET.get("address", "").strip()
    cnpj = clean_cnpj(request.GET.get("cnpj", "").strip())
    status = request.GET.get("status", "").strip()
    print(f"status: {status}")
    
    suppliers = Suppliers.objects.all()

    
    if fantasy_company_name:
        suppliers = suppliers.filter(Q(fantasy_name__icontains=fantasy_company_name) | Q(company_name__icontains=fantasy_company_name))
        
    if email:
        suppliers = suppliers.filter(Q(email__icontains=email))
    
    if address:
        suppliers = suppliers.filter(Q(city__icontains=address) | Q(state__icontains=address))

    if cnpj:
        print(cnpj)
        suppliers = suppliers.filter(cnpj=cnpj)
    
    if status == "Ativo":
        print("ffff")
        suppliers = suppliers.filter(enabled='1')
        
    if status == "Inativo":
        suppliers = suppliers.filter(enabled='0')


    paginator = Paginator(suppliers, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }
    
    return render(request, "suppliers/index.html", context)

@require_POST
def toggle_enabled(request, id):
    supplier = get_object_or_404(Suppliers, pk=id)

    supplier.enabled = not supplier.enabled
    supplier.save()

    return JsonResponse({ "message": "success"})

@require_POST
def delete(request, id):
    supplier = get_object_or_404(Suppliers, pk=id)
    supplier.delete()

    return redirect("suppliers:index")

def create(request):
    
    #POST
    if request.method == "POST":
        form = SuppliersForm(request.POST)
        
        if form.is_valid():
            form.save()

            messages.success(request, "Fornecedor cadastrado com sucesso!")
            return redirect("suppliers:index")


        messages.error(request, "Falha ao cadastrar o fornecedor. Verifique o preenchimento dos campos")
        context = { "form": form }        
        return render(request, "suppliers/create.html", context)
    
    #GET
    form = SuppliersForm()
    context = { "form": form }
    return render(request, "suppliers/create.html", context)

