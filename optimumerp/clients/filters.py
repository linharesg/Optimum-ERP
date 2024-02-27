from .models import Clients
import django_filters
from django.forms.widgets import TextInput
from django.db.models import Q

class ClientsFilter(django_filters.FilterSet):
    """
    Este filtro permite realizar consultas complexas em dados de clientes, incluindo pesquisa por razão social ou nome
    fantasia, estado, cidade, CNPJ, e-mail e status de ativação.

    Attributes:
        company_or_fantasy_name (CharFilter): Filtro para pesquisar por razão social ou nome fantasia.
        state (ChoiceFilter): Filtro para selecionar clientes por estado.
        city (CharFilter): Filtro para pesquisar clientes por cidade.
        cnpj (CharFilter): Filtro para pesquisar clientes por CNPJ.
        email (CharFilter): Filtro para pesquisar clientes por e-mail.
        enabled (ChoiceFilter): Filtro para selecionar clientes por status de ativação.

    Methods:
        company_or_fantasy_name_filter(): Método para filtrar clientes por razão social ou nome fantasia.
    """

    company_or_fantasy_name = django_filters.CharFilter(method='company_or_fantasy_name_filter', label="",  widget=TextInput(attrs={'placeholder': 'Razão social / Nome fantasia'}))
    state = django_filters.ChoiceFilter(field_name='state', label="", empty_label="Estado", choices=Clients.STATE_CHOICES)
    city = django_filters.CharFilter(field_name='city',label="", widget=TextInput(attrs={'placeholder': 'Cidade'}), lookup_expr='icontains')
    cnpj = django_filters.CharFilter(field_name='cnpj',label="", widget=TextInput(attrs={'placeholder': 'CNPJ'}))
    email = django_filters.CharFilter(field_name='email',label="", widget=TextInput(attrs={'placeholder': 'email@email.com'}), lookup_expr='icontains')
    enabled = django_filters.ChoiceFilter(field_name='enabled', label="", empty_label="Status", choices={True:"Ativo", False: "Inativo"})

    class Meta:
        """
        Metadados do filtro.

        Attributes:
            model (Model): O modelo associado ao filtro.
            fields (list): Lista de campos do modelo pelos quais será possível filtrar.
        """
        model = Clients
        fields = ['company_or_fantasy_name', 'cnpj', 'email', 'city', 'state', 'enabled' ]

    def company_or_fantasy_name_filter(self, queryset, name, value):
        """
        Filtra clientes por razão social ou nome fantasia.

        Args:
            queryset (QuerySet): Conjunto de objetos a serem filtrados.
            name (str): Nome do campo de filtro.
            value (str): Valor do filtro.

        Returns:
            QuerySet: Conjunto de objetos filtrados.
        """
        return queryset.filter(
            Q(company_name__icontains=value) |
            Q(fantasy_name__icontains=value)
        )