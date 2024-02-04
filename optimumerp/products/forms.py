from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["slug", "is_perishable"]

        labels = {
            "name": "Nome",
            "description": "Descrição",
            "sale_price": "Preço de venda",
            "expiration_date": "Data de expiração",
            "enabled": "Ativo",
            "category": "Categoria"
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
        }
        
        widgets = {
            "expiration_date": forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d")
        }