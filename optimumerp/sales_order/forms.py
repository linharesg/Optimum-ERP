from django import forms
from .models import SalesOrder, SalesOrderProduct
from crispy_forms.helper import FormHelper

class SalesOrderForm(forms.ModelForm):

    class Meta:
        model = SalesOrder
        exclude = ["products"]

        labels = {
            "status": "Status",
            "delivery_date": "Data de entrega",
            "total_value": "Valor total",
            "discount": "Desconto",
            "installments": "Parcelas",
            "created_at": "Data de emissão",
            "client": "Cliente",
            "products": "Produtos",
            "user": "Usuário solicitante"
        }

        widgets = {
            "delivery_date": forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d"),
            'status': forms.TextInput(attrs={'readonly': 'readonly'}),
            'total_value': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'user': forms.TextInput(attrs={'readonly': 'readonly'})
        }


class SalesOrderProductForm(forms.ModelForm):
    class Meta:
        model = SalesOrderProduct
        fields = "__all__"
        # exclude = ["status"]
        widgets = {
            "unit_value": forms.NumberInput(attrs={"placeholder": "Preço de custo"}),
            "amount": forms.NumberInput(attrs={"placeholder": "Quantidade"}),
            "total_value_product": forms.NumberInput(attrs={"placeholder": "Total", 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

SalesOrderProductFormSet = forms.inlineformset_factory(
    SalesOrder,
    SalesOrderProduct,
    form=SalesOrderProductForm,
    extra=1,
    can_delete=True,
    max_num=5
)