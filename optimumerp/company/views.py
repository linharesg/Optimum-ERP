from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Company
from .forms import CompanyForm

# Create your views here
def index(request):
    companies = Company.objects.all()

    context = {
        "companies": companies
        }
    
    return render(request, "company/index.html", context)