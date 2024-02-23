
import re
from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
       
    class Meta:
        model = Company
        exclude = ["slug"]
        
        labels = {
            "company_name": "Razão Social",
            "fantasy_name": "Nome fantasia",
            "state_registration": "Inscrição Estadual",
            "cnpj": "CNPJ",
            "email": "E-mail",
            "zipcode": "CEP",
            "street": "Rua",
            "number": "Número",
            "city": "Cidade",
            "state": "Estado",
            "phone": "Contato",
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