import django_filters
from django.forms.widgets import TextInput
from .models import Inventory

class InventoryFilter(django_filters.FilterSet):
    """
    Este filtro permite aos usuários pesquisar itens de inventário com base no nome do produto e na quantidade disponível. Ele fornece campos de filtro para especificar o nome do produto, a quantidade mínima e a quantidade máxima.

    Atributos:
        product (CharFilter): Filtro para pesquisar itens de inventário com base no nome do produto.
        qt_min (NumberFilter): Filtro para pesquisar itens de inventário com quantidade igual ou superior ao valor especificado.
        qt_max (NumberFilter): Filtro para pesquisar itens de inventário com quantidade igual ou inferior ao valor especificado.

    Meta:
        model (Model): O modelo associado a este filtro.
        fields (list): Lista de campos que podem ser usados como critérios de filtragem.
    """
    product = django_filters.CharFilter(field_name="product__name", label="", widget=TextInput(attrs={'placeholder': 'Produto'}), lookup_expr='icontains')
    qt_min = django_filters.NumberFilter(field_name="quantity", label="", widget=TextInput(attrs={'placeholder': 'De'}), lookup_expr='gte')
    qt_max = django_filters.NumberFilter(field_name="quantity", label="", widget=TextInput(attrs={'placeholder': 'até'}), lookup_expr='lte')
    class Meta:
        model = Inventory
        fields = ['product', 'qt_min', 'qt_max']