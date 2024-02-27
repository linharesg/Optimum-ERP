from django.db import models
from products.models import Product
from inventory.models import Inventory
from django.db import transaction
from .exceptions import TransactionQuantityError

class Transaction(models.Model):
    """
    Um modelo para registrar transações de entrada e saída de produtos.

    Este modelo mantém registros de transações, incluindo detalhes como o produto associado, a quantidade envolvida,
    o tipo de transação (entrada ou saída) e a data da transação.

    Attributes:
        TRANSACTION_TYPE_CHOICES (dict): Um dicionário que define as opções de tipos de transação disponíveis.
        product (ForeignKey): Uma chave estrangeira que relaciona a transação a um produto específico.
        quantity (DecimalField): Um campo que armazena a quantidade envolvida na transação.
        type (CharField): Um campo que armazena o tipo de transação (entrada ou saída).
        date (DateTimeField): Um campo que armazena a data e hora da transação.

    Methods:
        __str__: Retorna uma representação em string da transação.
        create: Método de classe para criar uma nova transação.

    """
    TRANSACTION_TYPE_CHOICES = {
        "IN": "Entrada",
        "OUT": "Saída"
    }

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=255, decimal_places=2)
    type = models.CharField(max_length=255, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Retorna uma representação em string da transação.

        Returns:
            str: Uma string que representa a transação no formato "Produto: <nome do produto> | Quantidade: <quantidade> | Tipo: <tipo> | Data: <data>".

        """
        return f"Produto: {self.product} | Quantidade: {self.quantity} | Tipo: {self.type} | Data: {self.date}"
    
    @classmethod
    def create(cls, product, quantity, type):
        """
        Este método cria uma nova transação com base nos parâmetros fornecidos e atualiza o inventário de acordo com o tipo de transação.

        Args:
            product (Product): O produto associado à transação.
            quantity (Decimal): A quantidade envolvida na transação.
            type (str): O tipo de transação (entrada ou saída).

        Raises:
            TransactionQuantityError: Se a quantidade de saída for maior do que a quantidade disponível no inventário.

        """
        inventory = Inventory.objects.get(product__id=product.id)
        with transaction.atomic():
            try:
                _transaction = Transaction.objects.create(product=product, quantity=quantity, type=type)
                if type == "OUT":
                    if inventory.quantity - quantity < 0:
                        transaction_error = TransactionQuantityError("Quantidade indisponível no estoque")
                        raise transaction_error
                    else:
                        inventory.quantity -= quantity
                        inventory.save()

                elif type == "IN":
                    inventory.quantity += quantity
                    inventory.save()
            except: 
                _transaction.delete()

        
    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"