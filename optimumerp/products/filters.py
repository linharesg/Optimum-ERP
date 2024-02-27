from .models import Product
import django_filters
from django.forms.widgets import TextInput


class ProductFilter(django_filters.FilterSet):
    """
    Filtro para buscar produtos com base em diferentes critérios.
    """
    name = django_filters.CharFilter(field_name='name', label="", widget=TextInput(attrs={'placeholder': 'Nome do produto'}), lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', label="", widget=TextInput(attrs={'placeholder': 'Descrição'}), lookup_expr='icontains')
    # category = django_filters.CharFilter(field_name='category',label="", widget=TextInput(attrs={'placeholder': 'Categoria'}), lookup_expr='icontains')
    unit_of_measurement = django_filters.ChoiceFilter(field_name='unit_of_measurement', empty_label="Unidade de medida", label="", choices=Product.MEASUREMENT_CHOICES)
    # expiration_date
    enabled = django_filters.ChoiceFilter(field_name='enabled', empty_label="Status", label="", choices={True:"Ativo", False: "Inativo"})
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'unit_of_measurement', 'enabled' ]
