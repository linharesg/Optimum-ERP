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

def update(request, id):
    company = Company.objects.get(id=id)

    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)

        if form.is_valid():
            form.save()
            messages.success(request, "Dados atualizados com sucesso!")
            return redirect("company:index")
        else:
            context = {
                "form": form,
            }
            return render(request, "company/update.html", context)
        
    else:
        form = CompanyForm(instance=company)
        context = {
            "form": form,
        }
    return render(request, 'company/update.html', context)