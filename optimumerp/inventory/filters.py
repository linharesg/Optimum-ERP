import django_filters
from django.forms.widgets import TextInput
from .models import Inventory

class InventoryFilter(django_filters.FilterSet):
    product = django_filters.CharFilter(field_name="product__name", label="", widget=TextInput(attrs={'placeholder': 'Produto'}), lookup_expr='icontains')
    qt_min = django_filters.NumberFilter(field_name="quantity", label="", widget=TextInput(attrs={'placeholder': 'De'}), lookup_expr='gte')
    qt_max = django_filters.NumberFilter(field_name="quantity", label="", widget=TextInput(attrs={'placeholder': 'até'}), lookup_expr='lte')
    class Meta:
        model = Inventory
        fields = ['product', 'qt_min', 'qt_max']