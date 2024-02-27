from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    """
    Um formulário para criar e atualizar instâncias de Category.

    Atributos:
        Meta: Uma classe interna do formulário que especifica o modelo associado e os campos que serão incluídos no formulário.
    """
    class Meta:
        """
        Classe interna que especifica o modelo associado e os campos que serão incluídos no formulário.

        Atributos:
            model (django.db.models.Model): O modelo associado ao formulário.
            fields (list): Uma lista de campos do modelo a serem incluídos no formulário. Se for '__all__', todos os campos serão incluídos.
            labels (dict, opcional): Um dicionário que mapeia os nomes dos campos do modelo para rótulos de campo personalizados.
        """
        model = Category
        fields = "__all__"
        labels = {
            "name": "Nome",
            "description": "Descrição"
        }