from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Category
from .forms import CategoryForm
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.decorators.http import require_POST


class CategoryListView(PermissionRequiredMixin, ListView):
    """
    Esta classe-based view é responsável por exibir uma lista paginada de categorias.
    Ela utiliza o modelo `Category` e o template `categories/index.html`.

    Attributes:
        model (Model): O modelo de dados associado à view.
        template_name (str): O nome do template usado para renderizar a página.
        paginate_by (int): O número de itens por página.
        permission_required (str): A permissão necessária para acessar esta view.

    """
    model = Category
    template_name = "categories/index.html"
    paginate_by = 100
    permission_required = "categories.view_category"

def create(request):
    """
    Esta função é responsável por criar uma nova categoria.
    Ela processa requisições POST para salvar a categoria no banco de dados.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.

    Returns:
        HttpResponse: Uma resposta HTTP que redireciona o usuário para a página de listagem de categorias ou exibe mensagens de erro.

    """
    form_action = reverse("categories:create")

    # POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()  # Salva a categoria no banco de dados
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
    """
    Esta função é responsável por atualizar uma categoria existente.
    Ela processa requisições POST para salvar as alterações no banco de dados.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        id (int): O ID da categoria a ser atualizada.

    Returns:
        HttpResponse: Uma resposta HTTP que redireciona o usuário para a página de listagem de categorias ou exibe mensagens de erro.

    """
    category = get_object_or_404(Category, id=id)
    form_action = reverse("categories:update", args=(id,))

    # POST
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, "Categoria atualizada com sucesso!")
            return redirect("categories:index")
        else:
            messages.error(request, "Erro ao atualizar a categoria. Verifique os dados informados.")

        context = {"form": form, "form_action": form_action}
        return render(request, "categories/create.html", context)

    # GET
    form = CategoryForm(instance=category)
    context = {"form": form, "form_action": form_action}
    return render(request, "categories/create.html", context)


@require_POST
def delete(request, id):
    """
    Esta função é responsável por excluir uma categoria existente.

    Args:
        request (HttpRequest): O objeto HttpRequest que contém os dados da solicitação.
        id (int): O ID da categoria a ser excluída.

    Returns:
        HttpResponseRedirect: Uma resposta HTTP que redireciona o usuário para a página de listagem de categorias após a exclusão.

    """
    category = get_object_or_404(Category, pk=id)
    category.delete()
    return redirect("categories:index")