from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Company
from .forms import CompanyForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """
    Exibe uma lista de todas as empresas cadastradas.
    
    Returns:
        HttpResponse: Uma resposta HTTP contendo a página HTML renderizada com a lista de empresas.
    """
    companies = Company.objects.all()

    context = {
        "companies": companies
    }
    
    return render(request, "company/index.html", context)