from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Category
from .forms import CategoryForm
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.decorators.http import require_POST

# Categories

class CategoryListView(PermissionRequiredMixin, ListView):
    model = Category
    template_name = "categories/index.html"
    paginate_by = 100
    permission_required = "categories.view_category"

def create(request):
    form_action = reverse("categories:create")

    # POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save() # Salva o produto no banco de dados
            messages.success(request, "A categoria foi cadastrada com sucesso!")
            return redirect("categories:index")
        
        messages.error(request, "Falha ao cadastrar a categoria. Verifique o preenchimento dos campos.")
        context = {"form": form, "form_action": form_action}
        return render(request, "categories/create.html", context)

    # GET
    form = CategoryForm()
    context = {"form": form, "form_action": form_action}
    return render(request, "categories/create.html", context)

def update(request, id):
    category = get_object_or_404(Category, id=id)
    form_action = reverse("categories:update", args=(id,))

    #POST 
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request,"Categoria atualizado com sucesso!")
            return redirect("categories:index")
        else:
            messages.error(request, "Erro ao atualizar a categoria. Verifique os dados informados.")
        
        context = {"form": form, "form_action": form_action}
        return render(request, "categories/create.html", context)
    
    # GET
    form =  CategoryForm(instance=category)
    context = {"form": form, "form_action": form_action}
    return render(request, "categories/create.html", context)

@require_POST
def delete(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()
    return redirect("categories:index")