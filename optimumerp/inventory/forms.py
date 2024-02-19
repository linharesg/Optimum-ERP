from django.forms import forms
from .models import Inventory

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