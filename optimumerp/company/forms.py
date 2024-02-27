import re
from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    """
    Este formulário é usado para coletar e validar dados relacionados a uma empresa, como razão social, nome fantasia,
    CNPJ, e-mail, endereço, entre outros.

    Attributes:
        clean_cnpj: Método para limpar e formatar o campo CNPJ.
        clean_phone: Método para limpar e formatar o campo de telefone.
        clean_zipcode: Método para limpar e formatar o campo de CEP.
    """

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
        """
        Limpa e formata o campo CNPJ, removendo caracteres não numéricos.
        """
        cnpj = self.cleaned_data.get("cnpj", "")
        cnpj = re.sub("[^0-9]", "", cnpj)
        
        return cnpj
    
    def clean_phone(self):
        """
        Limpa e formata o campo de telefone, removendo caracteres não numéricos.
        """
        phone = self.cleaned_data.get("phone", "")
        phone = re.sub("[^0-9]", "", phone)

        return phone

    def clean_zipcode(self):
        """
        Limpa e formata o campo de CEP, removendo caracteres não numéricos.
        """
        zipcode = self.cleaned_data.get("zipcode", "")
        zipcode = re.sub("[^0-9]", "", zipcode)

        return zipcode