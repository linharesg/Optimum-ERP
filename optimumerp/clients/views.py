from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .forms import ClientsForm
from .models import Clients
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import UpdateView
from sales_order.models import SalesOrder
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .filters import ClientsFilter

@login_required
def index(request):
    """
    View para exibir uma lista paginada de clientes e aplicar filtros.

    Retorna uma página HTML contendo uma lista paginada de clientes, com a opção de filtrar os clientes
    por diversos critérios.

    Args:
        request (HttpRequest): Requisição HTTP recebida pelo servidor.

    Returns:
        HttpResponse: Resposta HTTP contendo a página HTML com a lista de clientes e filtros aplicados.

    """
    clients = Clients.objects.order_by("-id")
    client_filter = ClientsFilter(request.GET, queryset=clients)

    paginator = Paginator(client_filter.qs, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        'filter': client_filter
    }
    
    return render(request, "clients/index.html", context)


class ClientsUpdateView(UpdateView):
    """
    View para atualizar informações de um cliente existente.

    Permite que um usuário atualize informações de um cliente existente por meio de um formulário HTML.
    Verifica se o cliente está associado a pedidos de vendas pendentes antes de inativá-lo.

    Attributes:
        model (Clients): Modelo do cliente a ser atualizado.
        template_name (str): Nome do template HTML a ser usado para renderizar a página.
        form_class (form): Classe do formulário a ser usado para processar os dados do cliente.
        success_url (str): URL para redirecionar o usuário após uma atualização bem-sucedida.

    Methods:
        form_valid(self, form): Executado quando o formulário é válido, verifica se há pedidos de vendas pendentes antes de inativar o cliente e envia uma mensagem de sucesso.
        form_invalid(self, form): Executado quando o formulário é inválido, envia uma mensagem de erro.

    """
    model = Clients
    template_name = "clients/update.html"
    form_class = ClientsForm
    success_url = reverse_lazy("clients:index")

    def form_valid(self, form):
        """
        Executado quando o formulário é válido.

        Verifica se há pedidos de vendas pendentes associados ao cliente antes de inativá-lo e envia uma mensagem de sucesso.

        Args:
            form (Form): Formulário contendo os dados atualizados do cliente.

        Returns:
            HttpResponse: Resposta HTTP após a atualização bem-sucedida do cliente.

        """
        client = form.instance
        pending_sale_order = SalesOrder.objects.filter(client=client, status="Pendente").aggregate(count=Count('id'))['count']
        if pending_sale_order > 0 and not client.enabled:
            messages.error(self.request, f"Não foi possível inativar o cliente, pois o mesmo está associado a um pedido de vendas pendente.")
            return super().form_invalid(form)

        response = super().form_valid(form)
        messages.success(self.request, "Cliente atualizado com sucesso!")
        return response

    def form_invalid(self, form):
        """
        Executado quando o formulário é inválido.

        Envia uma mensagem de erro após uma tentativa malsucedida de atualizar o cliente.

        Args:
            form (Form): Formulário contendo os dados do cliente.

        Returns:
            HttpResponse: Resposta HTTP após uma tentativa malsucedida de atualizar o cliente.

        """
        response = super().form_invalid(form)
        messages.error(self.request, "Erro ao atualizar o cliente!")
        return response


@require_POST
def toggle_enabled(request, id):
    """
    View para ativar ou desativar um cliente.

    Ativa ou desativa um cliente com base no ID fornecido na requisição.
    Verifica se há pedidos de vendas pendentes associados ao cliente antes de inativá-lo.

    Args:
        request (HttpRequest): Requisição HTTP recebida pelo servidor.
        id (int): ID do cliente a ser ativado ou desativado.

    Returns:
        JsonResponse: Resposta JSON indicando o resultado da operação.

    """
    client = get_object_or_404(Clients, pk=id)

    pending_sale_order = SalesOrder.objects.filter(client=client, status="Pendente").aggregate(count=Count('id'))['count']
    if pending_sale_order > 0:
        messages.error(request, f"Não foi possível inativar o cliente, pois o mesmo está associado a um pedido de vendas pendente.")
        return JsonResponse({ "message": "error" })

    client.enabled = not client.enabled
    client.save()

    return JsonResponse({ "message": "success"})

@require_POST
def delete(request, id):
    """
    View para excluir um cliente.

    Exclui um cliente com base no ID fornecido na requisição.
    Verifica se há pedidos de vendas associados ao cliente antes de excluí-lo.

    Args:
        request (HttpRequest): Requisição HTTP recebida pelo servidor.
        id (int): ID do cliente a ser excluído.

    Returns:
        HttpResponseRedirect: Redireciona o usuário de volta para a página anterior após a exclusão bem-sucedida do cliente.

    """
    client = get_object_or_404(Clients, pk=id)
    
    sale_order_count = SalesOrder.objects.filter(client=client).aggregate(count=Count('id'))['count']
    if sale_order_count > 0:
        messages.error(request, f"Não foi possível excluir o cliente, pois o mesmo já está associado a um pedido de vendas. Considere inativá-lo.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    client.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def create(request):
    """
    View para criar um novo cliente.

    Exibe um formulário HTML para o usuário preencher com os dados do novo cliente.
    Após o envio do formulário, processa os dados e cria o novo cliente.

    Args:
        request (HttpRequest): Requisição HTTP recebida pelo servidor.

    Returns:
        HttpResponse: Resposta HTTP contendo o formulário para criar um novo cliente.

    """
    #POST
    if request.method == "POST":
        form = ClientsForm(request.POST)
        
        if form.is_valid():
            form.save()

            messages.success(request, "Cliente cadastrado com sucesso!")
            return redirect("clients:index")


        messages.error(request, "Falha ao cadastrar o cliente. Verifique o preenchimento dos campos")
        context = { "form": form }        
        return render(request, "clients/create.html", context)
    
    #GET
    form = ClientsForm()
    context = { "form": form }
    return render(request, "clients/create.html", context)