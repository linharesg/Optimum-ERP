from .models import Clients
import django_filters
from django.forms.widgets import TextInput
from django.db.models import Q

class ClientsFilter(django_filters.FilterSet):
    company_or_fantasy_name = django_filters.CharFilter(method='company_or_fantasy_name_filter', label="",  widget=TextInput(attrs={'placeholder': 'Razão social / Nome fantasia'}))
    state = django_filters.ChoiceFilter(field_name='state', label="Estado", choices=Clients.STATE_CHOICES)
    city = django_filters.CharFilter(field_name='city',label="", widget=TextInput(attrs={'placeholder': 'Cidade'}), lookup_expr='icontains')
    cnpj = django_filters.CharFilter(field_name='cnpj',label="", widget=TextInput(attrs={'placeholder': 'CNPJ'}))
    email = django_filters.CharFilter(field_name='email',label="", widget=TextInput(attrs={'placeholder': 'email@email.com'}), lookup_expr='icontains')
    enabled = django_filters.ChoiceFilter(field_name='enabled', label="Status", choices={True:"Ativo", False: "Inativo"})
    #  widget do select
    class Meta:
        model = Clients
        fields = ['company_or_fantasy_name', 'cnpj', 'email', 'city', 'state', 'enabled' ]

    def company_or_fantasy_name_filter(self, queryset, name, value):
        return queryset.filter(
            Q(company_name__icontains=value) |
            Q(fantasy_name__icontains=value)
        )