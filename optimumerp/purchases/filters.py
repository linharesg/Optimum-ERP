from .models import Purchases
import django_filters
from django.forms.widgets import TextInput
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import Value
from django import forms

class PurchasesFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(field_name="status", empty_label="Status", label="", choices=Purchases.STATUS_CHOICES)
    supplier = django_filters.CharFilter(method='supplier_company_or_fantasy_name_filter', label="",  widget=TextInput(attrs={'placeholder': 'Fornecedor'}))
    user = django_filters.CharFilter(method='user_seller_filter', label="",  widget=TextInput(attrs={'placeholder': 'Comprador'}))
    product = django_filters.CharFilter(field_name="products__name", label="", widget=TextInput(attrs={'placeholder': 'Produto'}), lookup_expr='icontains')
    delivery_date = django_filters.DateFilter(field_name='delivery_date', label="Entrega até:", lookup_expr='lte', widget=forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d"))
    
    class Meta:
        model = Purchases
        fields = ['supplier', 'user', 'product', 'status']

    def supplier_company_or_fantasy_name_filter(self, queryset, name, value):
        return queryset.filter(
            Q(supplier__company_name__icontains=value) |
            Q(supplier__fantasy_name__icontains=value)
        )
        
    def user_seller_filter(self, queryset, name, value):
        return queryset.annotate(fullname=Concat('user__first_name', Value(' '), 'user__last_name')).filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(user__username__icontains=value) |
            Q(fullname__icontains=value)
        )