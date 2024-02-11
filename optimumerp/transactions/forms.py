from django import forms
from .models import Transaction
from products.models import ProductInventory, Product
from crispy_forms.helper import FormHelper

class TransactionsForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = ["date"]

        labels = {
            "product": "Produto",
            "type": "Tipo de movimentação",
            "quantity": "Quantidade"
        }

        error_messages = {
            "quantity": { 
                "max_digits": "Limite de 255 dígitos",
                "decimal_places": "Limite de casas decimais"
            }
        }

class ProductInventoryForm(forms.ModelForm):
    class Meta:
        model = ProductInventory
        exclude = ["product"]
        widgets = {
            "quantity": forms.NumberInput(attrs={"placeholder": "Quantidade"}),
            "local": forms.TextInput(attrs={"placeholder": "Local"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

ProductInventoryFormSet = forms.inlineformset_factory(
    Product,
    ProductInventory,
    form=ProductInventoryForm,
    extra=1,
    can_delete=False,
    max_num = 1
)