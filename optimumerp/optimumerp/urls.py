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
    path('dashboard/', include('dashboard.urls'))
]
