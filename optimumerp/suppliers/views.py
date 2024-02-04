from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import SuppliersForm
from .models import Suppliers
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib import messages

def index(request):
    suppliers = Suppliers.objects.order_by("-id")

    paginator = Paginator(suppliers, 2)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "suppliers": page_obj
    }
    
    return render(request, "suppliers/index.html", context)

def search(request):
    search_value = request.GET.get("q").strip()

    if not search_value:
        return redirect("suppliers:index")
    
    suppliers = Suppliers.objects.filter(Q(fantasy_name__icontains=search_value) | Q(company_name__icontains=search_value)).order_by("-id")

    paginator = Paginator(suppliers, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "suppliers": page_obj
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
    form_action = reverse("suppliers:create")

    if request.method == "POST":
        form = SuppliersForm(request.POST)
        
        if form.is_valid():
            form.save()

            # messages.success(request, "Fornecedor cadastrado com sucesso!")
            print("oi")
            return redirect("suppliers:index")
            print("oi1")

        messages.error(request, "Falha ao cadastrar o fornecedor. Verifique o preenchimento dos campos")
        context = { "form": form, "form_action": form_action}        
        return render(request, "suppliers/create.html", context)
    
    #GET
    form = SuppliersForm()
    context = {"form": form}
    return render(request, "suppliers/create.html", context)

