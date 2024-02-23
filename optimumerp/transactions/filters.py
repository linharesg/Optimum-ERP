import django_filters
from django.forms.widgets import TextInput
from .models import Transaction
from django.forms import DateInput

class TransactionsFilter(django_filters.FilterSet):
    product = django_filters.CharFilter(field_name="product__name", label="", widget=TextInput(attrs={'placeholder': 'Produto'}), lookup_expr='icontains')
    type = django_filters.ChoiceFilter(field_name='type', label="Tipo movimentação:", choices=Transaction.TRANSACTION_TYPE_CHOICES)
    date_min = django_filters.DateFilter(field_name='date', label="De:", lookup_expr='gte', widget=DateInput(attrs={"type":"date"}, format="%Y-%m-%d"))
    date_max = django_filters.DateFilter(field_name='date', label="Até:", lookup_expr='lte', widget=DateInput(attrs={"type":"date"}, format="%Y-%m-%d"))

    class Meta:
        model = Transaction
        fields = ['product', 'date_min', 'date_max', 'type']