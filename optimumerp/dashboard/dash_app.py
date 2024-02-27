import dash
from dash import dcc, html
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from django.db.models import Count, Sum
from suppliers.models import Suppliers
from purchases.models import Purchases
from inventory.models import Inventory
from sales_order.models import SalesOrder, SalesOrderProduct

# Crie um aplicativo Dash
app = DjangoDash("Dashboard")

# GRÁFICO DE FORNECEDORES POR ESTADO
@app.dash_app.callback(
    dash.dependencies.Output('suppliers-chart', 'figure'),
    []
)
def update_suppliers_chart():
    """
    Atualiza o gráfico que mostra a distribuição de fornecedores por estado.
    """
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

# GRÁFICO DE COMPRAS POR FORNECEDOR
@app.dash_app.callback(
    dash.dependencies.Output('purchases-chart', 'figure'),
    []
)
def update_purchases_chart():
    """
    Atualiza o gráfico que mostra o valor total de compras por fornecedor.
    """
    purchases_by_supplier = Purchases.objects.values('supplier__company_name').annotate(total_value=Sum('total_value'))

    suppliers = [p['supplier__company_name'] for p in purchases_by_supplier]
    total_values = [p['total_value'] for p in purchases_by_supplier]

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

# GRÁFICO DE TOP 10 CLIENTES QUE MAIS COMPRARAM
@app.dash_app.callback(
    dash.dependencies.Output('sales-chart', 'figure'),
    []
)
def update_sales_chart():
    """
    Atualiza o gráfico que mostra os top 10 clientes que mais compraram.
    """
    sales_by_client = SalesOrder.objects.values('client__company_name').annotate(total_value=Sum('total_value')).order_by('-total_value')[:10]

    clients = [s['client__company_name'] for s in sales_by_client]
    total_values = [s['total_value'] for s in sales_by_client]

    data = [
        go.Bar(
            x=total_values,
            y=clients,
            orientation='h'
        )
    ]
    layout = go.Layout(
        xaxis=dict(title='Total de Vendas'),
        yaxis=dict(title='Cliente')
    )

    return {'data': data, 'layout': layout}

# TOP 10 PRODUTOS MAIS VENDIDOS
@app.dash_app.callback(
    dash.dependencies.Output('top-products-chart', 'figure'),
    []
)
def create_top_products_chart():
    """
    Cria o gráfico dos top 10 produtos mais vendidos.
    """
    top_products = SalesOrderProduct.objects.values('product__name').annotate(total_sold=Sum('amount')).order_by('-total_sold')[:10]

    product_names = [item['product__name'] for item in top_products]
    total_sold = [item['total_sold'] for item in top_products]

    data = [
        go.Bar(
            x=total_sold,
            y=product_names,
            orientation='v'
        )
    ]
    layout = go.Layout(
        title='Top 10 Produtos Mais Vendidos',
        xaxis=dict(title='Quantidade Vendida'),
        yaxis=dict(title='Produto')
    )

    return {'data': data, 'layout': layout}

# GRÁFICO DE VENDAS POR USUÁRIO
@app.dash_app.callback(
    dash.dependencies.Output('sales-by-user-chart', 'figure'),
    []
)
def update_sales_by_user_chart():
    """
    Atualiza o gráfico que mostra as vendas por usuário.
    """
    sales_by_user = SalesOrder.objects.values('user__name').annotate(total_sales=Sum('total_value'))

    name = [item['user__name'] for item in sales_by_user]
    total_sales = [item['total_sales'] for item in sales_by_user]

    data = [
        go.Pie(
            labels=name,
            values=total_sales,
        )
    ]
    layout = go.Layout(
        title='Vendas por Usuário'
    )

    return {'data': data, 'layout': layout}

# GRÁFICO DE TOP 10 PRODUTOS COM MAIOR ESTOQUE
@app.dash_app.callback(
    dash.dependencies.Output('top-inventory-chart', 'figure'),
    []
)
def update_top_inventory_chart():
    """
    Atualiza o gráfico que mostra os top 10 produtos com maior estoque.
    """
    top_inventory = Inventory.objects.order_by('-quantity')[:10]

    product_names = [item.product.name for item in top_inventory]
    quantities = [item.quantity for item in top_inventory]

    data = [
        go.Bar(
            x=quantities,
            y=product_names,
            orientation='h'
        )
    ]
    layout = go.Layout(
        title='Top 10 Produtos com Maior Estoque',
        xaxis=dict(title='Quantidade em Estoque'),
        yaxis=dict(title='Produto')
    )

    return {'data': data, 'layout': layout}

# Crie o layout do Dash
app.layout = html.Div([
    html.H1('Dashboard'),

    # GRÁFICO DE TOP 10 CLIENTES QUE MAIS COMPRARAM
    dcc.Graph(id='sales-chart'),
        
    # GRÁFICO DE TOP 10 PRODUTOS MAIS VENDIDOS
    dcc.Graph(id='top-products-chart'),

    # GRÁFICO DE VENDAS POR POR USUÁRIO
    dcc.Graph(id='sales-by-user-chart'),

    # GRÁFICO DE FORNECEDORES POR ESTADO
    dcc.Graph(id='suppliers-chart'),
    
    # GRÁFICO DE COMPRAS POR FORNECEDOR
    dcc.Graph(id='purchases-chart'),

    # GRÁFICO DE TOP 10 PRODUTOS COM MAIOR ESTOQUE
    dcc.Graph(id='top-inventory-chart')
])