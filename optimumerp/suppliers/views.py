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
    """
    View para exibir uma lista paginada de fornecedores e aplicar filtros.

    Retorna uma página HTML contendo uma lista paginada de fornecedores, com a opção de filtrar os fornecedores
    por diversos critérios.

    Args:
        request (HttpRequest): Requisição HTTP recebida pelo servidor.

    Returns:
        HttpResponse: Resposta HTTP contendo a página HTML com a lista de fornecedores e filtros aplicados.

    """
    suppliers = Suppliers.objects.order_by("-id")
    supplier_filter = SuppliersFilter(request.GET, queryset=suppliers)

    # Aplicando a paginação
    paginator = Paginator(supplier_filter.qs, 50)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        'filter': supplier_filter
    }
    
    return render(request, "suppliers/index.html", context)


class SupplierUpdateView(UpdateView):
    """
    View para atualizar informações de um fornecedor existente.

    Permite que um usuário atualize informações de um fornecedor existente por meio de um formulário HTML.

    Attributes:
        model (Suppliers): Modelo do fornecedor a ser atualizado.
        template_name (str): Nome do template HTML a ser usado para renderizar a página.
        form_class (form): Classe do formulário a ser usado para processar os dados do fornecedor.
        success_url (str): URL para redirecionar o usuário após uma atualização bem-sucedida.

    Methods:
        form_valid(self, form): Executado quando o formulário é válido, envia uma mensagem de sucesso.
        form_invalid(self, form): Executado quando o formulário é inválido, envia uma mensagem de erro.

    """
    model = Suppliers
    template_name = "suppliers/update.html"
    form_class = SuppliersForm
    success_url = reverse_lazy("suppliers:index")

    def form_valid(self, form):
        """
        Executado quando o formulário é válido.

        Envia uma mensagem de sucesso após a atualização do fornecedor.

        Args:
            form (Form): Formulário contendo os dados atualizados do fornecedor.

        Returns:
            HttpResponse: Resposta HTTP após a atualização bem-sucedida do fornecedor.

        """
        response = super().form_valid(form)
        messages.success(self.request, "Fornecedor atualizado com sucesso!")
        return response

    def form_invalid(self, form):
        """
        Executado quando o formulário é inválido.

        Envia uma mensagem de erro após uma tentativa malsucedida de atualizar o fornecedor.

        Args:
            form (Form): Formulário contendo os dados do fornecedor.

        Returns:
            HttpResponse: Resposta HTTP após uma tentativa malsucedida de atualizar o fornecedor.

        """
        response = super().form_invalid(form)
        messages.error(self.request, "Erro ao atualizar o fornecedor!")
        return response


@require_POST
def toggle_enabled(request, id):
    """
    View para ativar ou desativar um fornecedor.

    Ativa ou desativa um fornecedor com base no ID fornecido na requisição.

    Args:
        request (HttpRequest): Requisição HTTP recebida pelo servidor.
        id (int): ID do fornecedor a ser ativado ou desativado.

    Returns:
        JsonResponse: Resposta JSON indicando o resultado da operação.

    """
    supplier = get_object_or_404(Suppliers, pk=id)

    supplier.enabled = not supplier.enabled
    supplier.save()

    return JsonResponse({ "message": "success"})


@require_POST
def delete(request, id):
    """
    View para excluir um fornecedor.

    Exclui um fornecedor com base no ID fornecido na requisição.

    Args:
        request (HttpRequest): Requisição HTTP recebida pelo servidor.
        id (int): ID do fornecedor a ser excluído.

    Returns:
        HttpResponseRedirect: Redireciona o usuário para a página de lista de fornecedores após a exclusão bem-sucedida.

    """
    supplier = get_object_or_404(Suppliers, pk=id)
    supplier.delete()

    return redirect("suppliers:index")


def create(request):
    """
    View para criar um novo fornecedor.

    Exibe um formulário HTML para o usuário preencher com os dados do novo fornecedor.
    Após o envio do formulário, processa os dados e cria o novo fornecedor.

    Args:
        request (HttpRequest): Requisição HTTP recebida pelo servidor.

    Returns:
        HttpResponse: Resposta HTTP contendo o formulário para criar um novo fornecedor.

    """
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