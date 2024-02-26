from django.db.models import Count, Sum
import plotly.graph_objs as go
from django.shortcuts import render
from suppliers.models import Suppliers
from purchases.models import Purchases
from sales_order.models import SalesOrder

def index(request):
    # GRÁFICO DE COMPRAS POR FORNECEDOR

    # Obtenha os dados de compra por fornecedor
    purchases_by_supplier = Purchases.objects.values('supplier__company_name').annotate(total_value=Sum('total_value'))

    # Extraia os nomes dos fornecedores e os valores totais
    suppliers = [p['supplier__company_name'] for p in purchases_by_supplier]
    total_values = [p['total_value'] for p in purchases_by_supplier]

    # Crie o gráfico de barras
    data = [
        go.Bar(
            x=suppliers,
            y=total_values,
        )
    ]
    layout = go.Layout(
        xaxis=dict(title='Fornecedor'),
        yaxis=dict(title='Valor Total das Compras')
    )

    chart = go.Figure(data=data, layout=layout)

    # Renderize o gráfico no HTML
    purchases_chart_data = chart.to_html(full_html=False)
    
    # GRÁFICO DE VENDAS POR CLIENTE
    # Consulta para obter as vendas por cliente
    sales_by_client = SalesOrder.objects.values('client__company_name').annotate(total_value=Sum('total_value')).order_by('-total_value')[:10]

    # Extrair os dados para o gráfico
    clients = [s['client__company_name'] for s in sales_by_client]
    total_values = [s['total_value'] for s in sales_by_client]

    # Criar o gráfico
    data = [
        go.Bar(
            x=total_values,
            y=clients,
            orientation='h'  # Define a orientação para horizontal
        )
    ]
    layout = go.Layout(
        xaxis=dict(title='Total de Vendas'),
        yaxis=dict(title='Cliente')
    )
    chart = go.Figure(data=data, layout=layout)
    sales_chart_html = chart.to_html(full_html=False)




    # GRÁFICO DE FORNECEDORES POR ESTADO
    suppliers_by_state = Suppliers.objects.values('state').annotate(count=Count('id'))
    states = [s['state'] for s in suppliers_by_state]
    counts = [s['count'] for s in suppliers_by_state]

    data = [
        go.Bar(
            x=states,
            y=counts,
        )
    ]

    layout = go.Layout(
        xaxis=dict(title='Estado'),
        yaxis=dict(title='Número de Fornecedores')
    )

    chart = go.Figure(data=data, layout=layout)
    supplier_chart_html = chart.to_html(full_html=False)

    context = {
        'purchases_chart_data': purchases_chart_data,
        'supplier_chart_html': supplier_chart_html,
        'sales_chart_html': sales_chart_html,
    }

    return render(request, "dashboard/index.html", context)