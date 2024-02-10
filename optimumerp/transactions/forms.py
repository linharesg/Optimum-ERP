from django import forms
from .models import Transaction

class TransactionsForm(forms.modelForm):

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