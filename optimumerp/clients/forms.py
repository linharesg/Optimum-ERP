
import re
from django import forms
from .models import Clients
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Hidden

class ClientsForm(forms.ModelForm):
       
    class Meta:
        model = Clients
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
            "phone": "Contato",
            "enabled": "Ativo"
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

    
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get("cnpj", "")
        cnpj = re.sub("[^0-9]", "", cnpj)
        
        return cnpj
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        phone = re.sub("[^0-9]", "", phone)

        return phone

    def clean_zipcode(self):
        zipcode = self.cleaned_data.get("zipcode", "")
        zipcode = re.sub("[^0-9]", "", zipcode)

        return zipcode