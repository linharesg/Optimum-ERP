class TransactionQuantityError(Exception):
    """
    Uma exceção personalizada para erros relacionados à quantidade em transações.

    Esta exceção é levantada quando ocorre um erro relacionado à quantidade em uma transação.

    Args:
        msg (str): A mensagem de erro associada à exceção.

    Methods:
        __init__(msg): Inicializa um objeto da classe TransactionQuantityError com a mensagem de erro fornecida.
        __str__(): Retorna a mensagem de erro como uma string.
        __repr__(): Retorna a mensagem de erro como uma representação de string.
    """
    def __init__(self, msg):
        """
        Inicializa um objeto da classe TransactionQuantityError com a mensagem de erro fornecida.

        Args:
            msg (str): A mensagem de erro associada à exceção.
        """
        self.msg = msg

    def __str__(self):
        """
        Retorna a mensagem de erro como uma string.
        
        Returns:
            str: A mensagem de erro.
        """
        return self.msg
    
    def __repr__(self):
        """
        Retorna a mensagem de erro como uma representação de string.
        
        Returns:
            str: A mensagem de erro.
        """
        return self.msg