from django.views.generic import TemplateView
from plotly.offline import plot
from plotly.graph_objects import Bar, Pie
from django.db.models import Sum
from suppliers.models import Suppliers
from purchases.models import Purchases
from inventory.models import Inventory
from sales_order.models import SalesOrder, SalesOrderProduct

class DashView(TemplateView):
    """
    View responsável por exibir o painel de controle com gráficos relacionados às vendas e estoque.
    """
    template_name = "dashboard/index.html"
    
    def get_context_data(self, **kwargs):
        """
        Obtém os dados necessários para renderizar os gráficos e adiciona ao contexto da view.
        """
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

        # Gráfico Top 10 produtos mais vendidos
        top_products = SalesOrderProduct.objects.values('product__name').annotate(total_sold=Sum('amount')).order_by('-total_sold')[:10]
        product_names = [item['product__name'] for item in top_products]
        total_sold = [item['total_sold'] for item in top_products]
        plot_div_salesproduct = plot([Bar(x=total_sold, y=product_names, orientation='v')], output_type="div", include_plotlyjs=False)

        # Gráfico Vendas por Usuário/Vendedor
        sales_by_user = SalesOrder.objects.values('user__name').annotate(total_sales=Sum('total_value'))
        name = [item['user__name'] for item in sales_by_user]
        total_sales = [item['total_sales'] for item in sales_by_user]
        plot_div_salesusers = plot([Pie(labels=name, values=total_sales)], output_type="div", include_plotlyjs=False)

        # Gráfico Top 10 Produtos com maior estoque
        top_inventory = Inventory.objects.order_by('-quantity')[:10]
        product_names = [item.product.name for item in top_inventory]
        quantities = [item.quantity for item in top_inventory]
        plot_div_inventory = plot([Bar(x=quantities, y=product_names, orientation='h')], output_type="div", include_plotlyjs=False)

        context["plot_div_purchases"] = plot_div_purchases
        context["plot_div_sales"] = plot_div_sales
        context["plot_div_suppliers"] = plot_div_suppliers
        context["plot_div_salesproduct"] = plot_div_salesproduct
        context["plot_div_salesusers"] = plot_div_salesusers
        context["plot_div_inventory"] = plot_div_inventory

        return context