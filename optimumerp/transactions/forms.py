from django import forms
from .models import Transaction, Inventory
from products.models import Product
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

class InventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory
        fields = "__all__"
        labels = {
            "product": "Produto",
            "quantity": "Quantidade",
        }

        error_messages = {
            "product": {
                "unique": "Este produto já está cadastrado no inventário",
                "required": "O campo nome é obrigatório"
            },
            "description": {
                "required": "O campo descrição é obrigatório"
            }
        }