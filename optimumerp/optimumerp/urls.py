"""
URL configuration for optimumerp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fornecedores/', include('suppliers.urls')),
    path('produtos/', include("products.urls")),
    path('transacoes/', include("transactions.urls")),
    path('estoque/', include("inventory.urls")),
    path("clientes/", include("clients.urls")),
    path("pedidos-de-venda/", include("sales_order.urls")),
    path('', include('users.urls')),
    path('nota-fiscal/', include('invoices.urls')),
    path("pedidos-de-compras/", include("purchases.urls")),
    path('empresa/', include("company.urls")),
    path('dashboard/', include('dashboard.urls')),
]
