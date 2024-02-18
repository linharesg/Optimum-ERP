from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from .forms import ClientsForm
from .models import Clients
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import UpdateView

def index(request):
    clients = Clients.objects.order_by("-id")

    paginator = Paginator(clients, 2)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj
    }
    
    return render(request, "clients/index.html", context)

class ClientsUpdateView(UpdateView):
    model = Clients
    template_name = "clients/update.html"
    form_class = ClientsForm
    success_url = reverse_lazy("clients:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cliente atualizado com sucesso!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.success(self.request, "Erro ao atualizar o cliente!")
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

    client.enabled = not client.enabled
    client.save()

    return JsonResponse({ "message": "success"})

@require_POST
def delete(request, id):
    client = get_object_or_404(Clients, pk=id)
    client.delete()

    return redirect("clients:index")

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

