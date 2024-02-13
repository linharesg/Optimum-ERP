from django import forms
from .models import Product, SupplierProduct
from crispy_forms.helper import FormHelper

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["slug", "is_perishable"]

        labels = {
            "name": "Nome",
            "description": "Descrição",
            "category": "Categoria",
            "sale_price": "Preço de venda",
            "cst": "Código de situação tributária (CST)",
            "minimum_stock": "Estoque mínimo",
            "unit_of_measurement": "Unidade de medida",
            "expiration_date": "Data de expiração",
            "enabled": "Ativo"
        }

        error_messages = {
            "name": {
                "unique": "Já existe um produto cadastrado com esse nome",
                "required": "O campo nome é obrigatório"
            },
            "description": {
                "required": "O campo descrição é obrigatório"
            },
            "sale_price": {
                "required": "O campo preço de venda é obrigatório",
            },
            "unit_of_measurement": {
                "required": "O campo de unidade de medida é obrigatório"
            },
            "cst": {
                "required": "O campo de CST é obrigatório"
            }
        }
        
        widgets = {
            "expiration_date": forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d")
        }

class SupplierProductForm(forms.ModelForm):
    class Meta:
        model = SupplierProduct
        exclude = ["product"]
        widgets = {
            "cost_price": forms.NumberInput(attrs={"placeholder": "Preço de custo"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

SupplierProductFormSet = forms.inlineformset_factory(
    Product,
    SupplierProduct,
    form=SupplierProductForm,
    extra=1,
    can_delete=True,
    max_num=5
)
