from django.views.generic import TemplateView
from plotly.offline import plot
from plotly.graph_objects import Bar
from django.db.models import Sum
from suppliers.models import Suppliers
from purchases.models import Purchases
from sales_order.models import SalesOrder

class DashView(TemplateView):
    template_name = "dashboard/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Gráfico de Compras por Fornecedor
        purchases_by_supplier = Purchases.objects.values('supplier__company_name').annotate(total_value=Sum('total_value'))
        suppliers = [p['supplier__company_name'] for p in purchases_by_supplier]
        total_values = [p['total_value'] for p in purchases_by_supplier]
        plot_div_purchases = plot([Bar(x=suppliers, y=total_values)], output_type="div", include_plotlyjs=False)

        # Gráfico de Vendas por Cliente
        sales_by_client = SalesOrder.objects.values('client__company_name').annotate(total_value=Sum('total_value')).order_by('-total_value')[:10]
        clients = [s['client__company_name'] for s in sales_by_client]
        total_values_sales = [s['total_value'] for s in sales_by_client]
        plot_div_sales = plot([Bar(x=total_values_sales, y=clients, orientation='h')], output_type="div", include_plotlyjs=False)

        # Gráfico de Fornecedores por Estado
        suppliers_by_state = Suppliers.objects.values('state').annotate(count=Sum('id'))
        states = [s['state'] for s in suppliers_by_state]
        counts = [s['count'] for s in suppliers_by_state]
        plot_div_suppliers = plot([Bar(x=states, y=counts)], output_type="div", include_plotlyjs=False)

        context["plot_div_purchases"] = plot_div_purchases
        context["plot_div_sales"] = plot_div_sales
        context["plot_div_suppliers"] = plot_div_suppliers

        return context