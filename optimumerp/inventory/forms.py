from django.forms import forms
from .models import Inventory

class InventoryForm(forms.ModelForm):
    """
    Este formulário permite aos usuários adicionar ou editar um item de inventário, associando um produto e especificando a quantidade disponível desse produto em estoque.

    Atributos:
        model (Model): O modelo associado a este formulário.
        fields (list): Lista de campos a serem incluídos no formulário. Neste caso, todos os campos do modelo `Inventory` são incluídos.
        labels (dict): Dicionário que mapeia os rótulos dos campos do formulário para rótulos personalizados.
        error_messages (dict): Dicionário que especifica mensagens de erro personalizadas para os campos do formulário.

    Meta:
        model (Model): O modelo associado a este formulário.
        fields (list): Lista de campos a serem incluídos no formulário. Neste caso, todos os campos do modelo `Inventory` são incluídos.
        labels (dict): Dicionário que mapeia os rótulos dos campos do formulário para rótulos personalizados.
        error_messages (dict): Dicionário que especifica mensagens de erro personalizadas para os campos do formulário.
    """

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