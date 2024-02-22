from .models import Suppliers
import django_filters
from django.forms.widgets import TextInput

class SuppliersFilter(django_filters.FilterSet):
    company_name = django_filters.CharFilter(field_name='company_name', label="", widget=TextInput(attrs={'placeholder': 'Razão social'}), lookup_expr='icontains')
    state = django_filters.ChoiceFilter(field_name='state', label="Estado", choices=Suppliers.STATE_CHOICES)
    city = django_filters.CharFilter(field_name='city',label="", widget=TextInput(attrs={'placeholder': 'Cidade'}), lookup_expr='icontains')
    cnpj = django_filters.CharFilter(field_name='cnpj',label="", widget=TextInput(attrs={'placeholder': 'CNPJ'}))
    email = django_filters.CharFilter(field_name='email',label="", widget=TextInput(attrs={'placeholder': 'email@email.com'}), lookup_expr='icontains')
    enabled = django_filters.ChoiceFilter(field_name='enabled', label="Status", choices={True:"Ativo", False: "Inativo"})

    class Meta:
        model = Suppliers
        fields = ['company_name', 'cnpj', 'email', 'city', 'state', 'enabled' ]