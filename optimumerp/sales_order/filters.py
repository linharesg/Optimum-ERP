from .models import SalesOrder
import django_filters
from django.forms.widgets import TextInput
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import Value, F
from django import forms

class SalesOrderFilter(django_filters.FilterSet):
    """
    Filtros para os pedidos de venda.

    Attributes:
        status (ChoiceFilter): Filtro de escolha para o status do pedido.
        costumer_company_or_fantasy_name (CharFilter): Filtro para o nome ou razão social do cliente.
        user (CharFilter): Filtro para o nome do vendedor.
        product (CharFilter): Filtro para o nome do produto no pedido.
        delivery_date (DateFilter): Filtro para a data de entrega até a data especificada.
    """
    status = django_filters.ChoiceFilter(
        field_name="status",
        empty_label="Status",
        label="",
        choices=SalesOrder.STATUS_CHOICES
    )
    costumer_company_or_fantasy_name = django_filters.CharFilter(
        method='costumer_company_or_fantasy_name_filter',
        label="",
        widget=TextInput(attrs={'placeholder': 'Cliente'})
    )
    user = django_filters.CharFilter(
        method='user_seller_filter',
        label="",
        widget=TextInput(attrs={'placeholder': 'Vendedor'})
    )
    product = django_filters.CharFilter(
        field_name="products__name",
        label="",
        widget=TextInput(attrs={'placeholder': 'Produto'}),
        lookup_expr='icontains'
    )
    delivery_date = django_filters.DateFilter(
        field_name='delivery_date',
        label="Entrega até:",
        lookup_expr='lte',
        widget=forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d")
    )
    
    class Meta:
        model = SalesOrder
        fields = ['costumer_company_or_fantasy_name', 'user', 'product', 'status']

    def costumer_company_or_fantasy_name_filter(self, queryset, name, value):
        """
        Filtra os pedidos pelo nome ou razão social do cliente.

        Args:
            queryset (QuerySet): Conjunto de dados a ser filtrado.
            name (str): Nome do campo de filtro.
            value (str): Valor do filtro.

        Returns:
            QuerySet: Conjunto de dados filtrado pelo nome ou razão social do cliente.
        """
        return queryset.filter(
            Q(client__company_name__icontains=value) |
            Q(client__fantasy_name__icontains=value)
        )
        
    def user_seller_filter(self, queryset, name, value):
        """
        Filtra os pedidos pelo nome do vendedor.

        Args:
            queryset (QuerySet): Conjunto de dados a ser filtrado.
            name (str): Nome do campo de filtro.
            value (str): Valor do filtro.

        Returns:
            QuerySet: Conjunto de dados filtrado pelo nome do vendedor.
        """
        return queryset.annotate(fullname=Concat('user__first_name', Value(' '), 'user__last_name')).filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(user__username__icontains=value) |
            Q(fullname__icontains=value)
        )