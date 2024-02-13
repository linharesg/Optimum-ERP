from django import forms
from .models import Transaction
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
