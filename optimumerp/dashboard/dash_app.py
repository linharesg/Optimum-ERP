import dash
from dash import dcc, html
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from django.db.models import Count, Sum
from suppliers.models import Suppliers
from purchases.models import Purchases
from sales_order.models import SalesOrder

# Crie um aplicativo Dash
app = DjangoDash("Dashboard")

# GRÁFICO DE COMPRAS POR FORNECEDOR
@app.dash_app.callback(
    dash.dependencies.Output('purchases-chart', 'figure'),
    []
)
def update_purchases_chart():
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

    return {'data': data, 'layout': layout}


# GRÁFICO DE VENDAS POR CLIENTE
@app.dash_app.callback(
    dash.dependencies.Output('sales-chart', 'figure'),
    []
)
def update_sales_chart():
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

    return {'data': data, 'layout': layout}


# GRÁFICO DE FORNECEDORES POR ESTADO
@app.dash_app.callback(
    dash.dependencies.Output('suppliers-chart', 'figure'),
    []
)
def update_suppliers_chart():
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

    return {'data': data, 'layout': layout}


# Crie o layout do Dash
app.layout = html.Div([
    html.H1('Dashboard'),

    # GRÁFICO DE COMPRAS POR FORNECEDOR
    dcc.Graph(id='purchases-chart'),

    # GRÁFICO DE VENDAS POR CLIENTE
    dcc.Graph(id='sales-chart'),

    # GRÁFICO DE FORNECEDORES POR ESTADO
    dcc.Graph(id='suppliers-chart')
])