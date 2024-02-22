from django.forms import Field
from .models import Clients
import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.forms.widgets import TextInput, Select

class ClientsFilter(django_filters.FilterSet):
    company_name = django_filters.CharFilter(field_name='company_name', label="", widget=TextInput(attrs={'placeholder': 'Razão social'}))
    state = django_filters.ChoiceFilter(field_name='state', label="Estado", choices=Clients.STATE_CHOICES)
    city = django_filters.CharFilter(field_name='city',label="", widget=TextInput(attrs={'placeholder': 'Cidade'}))
    cnpj = django_filters.CharFilter(field_name='cnpj',label="", widget=TextInput(attrs={'placeholder': 'CNPJ'}))
    email = django_filters.CharFilter(field_name='email',label="", widget=TextInput(attrs={'placeholder': 'email@email.com'}))
    enabled = django_filters.ChoiceFilter(field_name='enabled', label="Status", choices={True:"Ativo", False: "Inativo"})
    #  widget do select
    class Meta:
        model = Clients
        fields = ['company_name', 'cnpj', 'email', 'city', 'state', 'enabled' ]
