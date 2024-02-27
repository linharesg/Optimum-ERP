import re
from django import forms
from .models import Clients


class ClientsForm(forms.ModelForm):
    """
    Este formulário é utilizado para criar ou atualizar informações de clientes, incluindo razão social, nome fantasia,
    CNPJ, e-mail, endereço, telefone, entre outros.

    Attributes:
        Meta (nested class): Define os metadados do formulário, incluindo o modelo associado, os campos a serem excluídos,
            os rótulos dos campos e mensagens de erro personalizadas.

    Methods:
        clean_cnpj(): Limpa e formata o CNPJ, removendo caracteres não numéricos.
        clean_phone(): Limpa e formata o número de telefone, removendo caracteres não numéricos.
        clean_zipcode(): Limpa e formata o CEP, removendo caracteres não numéricos.
    """

    class Meta:
        """
        Metadados do formulário.

        Attributes:
            model (Model): O modelo associado ao formulário.
            exclude (list): Lista de campos a serem excluídos do formulário.
            labels (dict): Dicionário que mapeia os nomes dos campos para rótulos personalizados.
            error_messages (dict): Dicionário que define mensagens de erro personalizadas para campos específicos.
        """
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
        """
        Limpa e formata o CNPJ, removendo caracteres não numéricos.

        Returns:
            str: CNPJ formatado.
        """
        cnpj = self.cleaned_data.get("cnpj", "")
        cnpj = re.sub("[^0-9]", "", cnpj)
        
        return cnpj
    
    def clean_phone(self):
        """
        Limpa e formata o número de telefone, removendo caracteres não numéricos.

        Returns:
            str: Número de telefone formatado.
        """
        phone = self.cleaned_data.get("phone", "")
        phone = re.sub("[^0-9]", "", phone)

        return phone

    def clean_zipcode(self):
        """
        Limpa e formata o CEP, removendo caracteres não numéricos.

        Returns:
            str: CEP formatado.
        """
        zipcode = self.cleaned_data.get("zipcode", "")
        zipcode = re.sub("[^0-9]", "", zipcode)

        return zipcode