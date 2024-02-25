from django.shortcuts import render, redirect
from .models import Inventory
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    inventory = Inventory.objects.all()

    context = {
        "inventory": inventory
    }

    return render(request, "inventory/index.html", context)

def search(request):
    search_value = request.GET.get("q").strip()


    if not search_value:
        return redirect("inventory:index")
    
    inventory = Inventory.objects\
        .filter(Q(product__icontains=search_value) | Q(quantity__icontains=search_value))\
        .order_by("-product")
    
    context = {
        "inventory": inventory
    }

    return render(request, "inventory/index.html", context)
