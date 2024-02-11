from django import forms
from .models import Suppliers

class SuppliersForm(forms.ModelForm):
       
    class Meta:
        model = Suppliers
        # fields = "__all__"
        exclude = ["slug"]
        
        labels = {
            "company_name": "Razão Social",
            "fantasy_name": "Nome fantasia",
            "representative": "Representante",
            "cnpj": "CNPJ",
            "email": "E-mail",
            "zipcode": "CEP",
            "street": "Rua",
            "number": "Número",
            "city": "Cidade",
            "state": "Estado",
            "phone": "Contato"

        }
        
        error_messages = {
            "fantasy_name": { 
                "unique": "O fornecedor com esta razão social já está cadastrado",
                "max_length": "Limite de 255 caracteres.",
                "required": "O campo é obrigatório",
            },
            "email": {
                "unique": "Já existe um fornecedor com este e-mail."
            }
        }

    