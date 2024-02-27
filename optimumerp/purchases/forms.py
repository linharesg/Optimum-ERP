from django import forms
from .models import Purchases, PurchasesProduct
from crispy_forms.helper import FormHelper
from suppliers.models import Suppliers
from products.models import Product

class PurchasesForm(forms.ModelForm):

    class Meta:
        model = Purchases
        exclude = ["products"]

        labels = {
            "status": "Status",
            "delivery_date": "Data de entrega",
            "total_value": "Valor total",
            "discount": "Desconto(%)",
            "installments": "Parcelas",
            "created_at": "Data de emissão",
            "supplier": "Fornecedor",
            "products": "Produtos",
            "user": "Usuário solicitante"
        }

        widgets = {
            "delivery_date": forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d"),
            'status': forms.TextInput(attrs={'readonly': 'readonly'}),
            'total_value': forms.TextInput(attrs={'readonly': 'readonly'}),
            'user': forms.TextInput(attrs={'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["supplier"].queryset = Suppliers.objects.filter(enabled=True)

class PurchasesProductForm(forms.ModelForm):
    class Meta:
        model = PurchasesProduct
        fields = "__all__"

        widgets = {
            "unit_value": forms.NumberInput(attrs={"placeholder": "Preço de custo"}),
            "amount": forms.NumberInput(attrs={"placeholder": "Quantidade"}),
            "total_value_product": forms.NumberInput(attrs={"placeholder": "Total", "readonly": "readonly"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["product"].queryset = Product.objects.filter(enabled=True)
        self.helper.form_show_labels = False

PurchasesProductFormSet = forms.inlineformset_factory(
    Purchases,
    PurchasesProduct,
    form=PurchasesProductForm,
    extra=1,
    can_delete=True,
    max_num=1
)