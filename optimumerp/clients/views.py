from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from .forms import ClientsForm
from .models import Clients
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import UpdateView
from sales_order.models import SalesOrder
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Count
from django.contrib import messages

from .filters import ClientsFilter

def index(request):
    clients = Clients.objects.order_by("-id")
    client_filter = ClientsFilter(request.GET, queryset=clients)

    paginator = Paginator(client_filter.qs, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        'filter': client_filter
    }
    
    return render(request, "clients/index.html", context)


class ClientsUpdateView(UpdateView):
    model = Clients
    template_name = "clients/update.html"
    form_class = ClientsForm
    success_url = reverse_lazy("clients:index")

    def form_valid(self, form):
        client = form.instance
        pending_sale_order = SalesOrder.objects.filter(client=client, status="Pendente").aggregate(count=Count('id'))['count']
        if pending_sale_order > 0 and not client.enabled:
            messages.error(self.request, f"Não foi possível inativar o cliente, pois o mesmo está associado a um pedido de vendas pendente.")
            return super().form_invalid(form)

        response = super().form_valid(form)
        messages.success(self.request, "Cliente atualizado com sucesso!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Erro ao atualizar o cliente!")
        return response


def search(request):
    search_value = request.GET.get("q").strip()
    
    if not search_value:
        return redirect("clients:index")
    
    clients = Clients.objects.filter(Q(fantasy_name__icontains=search_value) | Q(company_name__icontains=search_value)).order_by("-id")
    print(clients)
    paginator = Paginator(clients, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }
    
    return render(request, "clients/index.html", context)

@require_POST
def toggle_enabled(request, id):
    client = get_object_or_404(Clients, pk=id)

    pending_sale_order = SalesOrder.objects.filter(client=client, status="Pendente").aggregate(count=Count('id'))['count']
    if pending_sale_order > 0:
        messages.error(request, f"Não foi possível inativar o cliente, pois o mesmo stá associado a um pedido de vendas pendente.")
        return JsonResponse({ "message": "error" })

    client.enabled = not client.enabled
    client.save()

    return JsonResponse({ "message": "success"})

@require_POST
def delete(request, id):
    client = get_object_or_404(Clients, pk=id)
    
    sale_order_count = SalesOrder.objects.filter(client=client).aggregate(count=Count('id'))['count']
    if sale_order_count > 0:
        messages.error(request, f"Não foi possível excluir o cliente, pois o mesmo já está associado a um pedido de vendas. Considere inativá-lo.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    client.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def create(request):
    
    #POST
    form_action = reverse("clients:create")

    if request.method == "POST":
        form = ClientsForm(request.POST)
        
        if form.is_valid():
            form.save()

            messages.success(request, "Cliente cadastrado com sucesso!")
            return redirect("clients:index")


        messages.error(request, "Falha ao cadastrar o cliente. Verifique o preenchimento dos campos")
        context = { "form": form, "form_action": form_action}        
        return render(request, "clients/create.html", context)
    
    #GET
    form = ClientsForm()
    context = { "form": form, "form_action": form_action }
    return render(request, "clients/create.html", context)

def search_teste(request):
    client_list = Clients.objects.all()
    print(client_list)
    client_filter = ClientsFilter(request.GET, queryset=client_list)
    # return render(request, 'clients/client_list.html', {'filter': client_filter})
    return render(request, 'clients/index.html', {'filter': client_filter})
