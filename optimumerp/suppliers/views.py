from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .forms import SuppliersForm
from .models import Suppliers
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import UpdateView
from .filters import SuppliersFilter
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    suppliers = Suppliers.objects.order_by("-id")
    supplier_filter = SuppliersFilter(request.GET, queryset=suppliers)

    paginator = Paginator(supplier_filter.qs, 2)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        'filter': supplier_filter
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

