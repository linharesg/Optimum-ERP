import django_filters
from django.forms.widgets import TextInput
from .models import Transaction
from django.forms import DateInput

class TransactionsFilter(django_filters.FilterSet):
    """
    Este filtro permite filtrar transações com base no nome do produto, tipo de transação e intervalo de datas.

    Attributes:
        product: Um filtro de caractere para o nome do produto.
        type: Um filtro de escolha para o tipo de transação.
        date_min: Um filtro de data para definir a data mínima da transação.
        date_max: Um filtro de data para definir a data máxima da transação.

    Methods:
        __init__(**kwargs): Inicializa um objeto da classe TransactionsFilter com os argumentos fornecidos.
    """
    product = django_filters.CharFilter(field_name="product__name", label="", widget=TextInput(attrs={'placeholder': 'Produto'}), lookup_expr='icontains')
    type = django_filters.ChoiceFilter(field_name='type', empty_label="Tipo movimentação:", label="", choices=Transaction.TRANSACTION_TYPE_CHOICES)
    date_min = django_filters.DateFilter(field_name='date', label="De:", lookup_expr='gte', widget=DateInput(attrs={"type":"date"}, format="%Y-%m-%d"))
    date_max = django_filters.DateFilter(field_name='date', label="Até:", lookup_expr='lte', widget=DateInput(attrs={"type":"date"}, format="%Y-%m-%d"))

    class Meta:
        """
        Metadados para a classe TransactionsFilter.

        Attributes:
            model: O modelo associado ao filtro.
            fields: Os campos do modelo que podem ser filtrados.
        """
        model = Transaction
        fields = ['product', 'date_min', 'date_max', 'type']