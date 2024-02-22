from .models import SalesOrder
import django_filters
from django.forms.widgets import TextInput
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import Value, F

class SalesOrderFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(field_name="status", label="Status", choices=SalesOrder.STATUS_CHOICES)
    costumer_company_or_fantasy_name = django_filters.CharFilter(method='costumer_company_or_fantasy_name_filter', label="",  widget=TextInput(attrs={'placeholder': 'Razão social / Nome fantasia'}))
    user = django_filters.CharFilter(method='user_seller_filter', label="",  widget=TextInput(attrs={'placeholder': 'Vendedor'}))
    product = django_filters.CharFilter(field_name="products__name", label="", widget=TextInput(attrs={'placeholder': 'Produto'}), lookup_expr='icontains')
    delivery_date = django_filters.DateFilter(field_name='delivery_date', label="Entrega até:", lookup_expr='lte')
    
    class Meta:
        model = SalesOrder
        fields = ['costumer_company_or_fantasy_name', 'user', 'product', 'status']

    def costumer_company_or_fantasy_name_filter(self, queryset, name, value):
        return queryset.filter(
            Q(client__company_name__icontains=value) |
            Q(client__fantasy_name__icontains=value)
        )
        
    def user_seller_filter(self, queryset, name, value):
        return queryset.annotate(fullname=Concat('user__first_name', Value(' '), 'user__last_name')).filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(user__username__icontains=value) |
            Q(fullname__icontains=value)
        )