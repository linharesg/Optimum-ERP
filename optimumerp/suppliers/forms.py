import re
from django import forms
from .models import Suppliers

class SuppliersForm(forms.ModelForm):
    """
    Formulário para criar e atualizar fornecedores.

    Atributos:
        Meta: Classe aninhada que define os metadados do formulário, incluindo o modelo e os campos a serem excluídos.
        labels (dict): Dicionário que mapeia os nomes dos campos do formulário para rótulos personalizados.
        error_messages (dict): Dicionário que define mensagens de erro personalizadas para os campos do formulário.

    Métodos:
        clean_cnpj(self): Método para limpar e formatar o CNPJ inserido pelo usuário.
        clean_phone(self): Método para limpar e formatar o número de telefone inserido pelo usuário.
        clean_zipcode(self): Método para limpar e formatar o CEP inserido pelo usuário.
    """
    class Meta:
        model = Suppliers
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
        """
        Limpa e formata o CNPJ inserido pelo usuário.

        Returns:
            str: CNPJ formatado.
        """
        cnpj = self.cleaned_data.get("cnpj", "")
        cnpj = re.sub("[^0-9]", "", cnpj)
        
        return cnpj
    
    def clean_phone(self):
        """
        Limpa e formata o número de telefone inserido pelo usuário.

        Returns:
            str: Número de telefone formatado.
        """
        phone = self.cleaned_data.get("phone", "")
        phone = re.sub("[^0-9]", "", phone)

        return phone

    def clean_zipcode(self):
        """
        Limpa e formata o CEP inserido pelo usuário.

        Returns:
            str: CEP formatado.
        """
        zipcode = self.cleaned_data.get("zipcode", "")
        zipcode = re.sub("[^0-9]", "", zipcode)

        return zipcode