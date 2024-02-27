from django import forms
from .models import Transaction
from products.models import Product
from crispy_forms.helper import FormHelper

class TransactionsForm(forms.ModelForm):
    """
    Este formulário é usado para criar e atualizar transações.

    Attributes:
        Meta: Uma classe interna que define os metadados do formulário.

    """
    class Meta:
        """
        Metadados para a classe TransactionsForm.

        Attributes:
            model: O modelo associado ao formulário.
            exclude: Lista de campos a serem excluídos do formulário.
            labels: Um dicionário que mapeia os rótulos dos campos do formulário.
            error_messages: Um dicionário que mapeia mensagens de erro personalizadas para campos específicos do formulário.
        """
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