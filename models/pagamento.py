from datetime import datetime
from enum import Enum

class TipoPagamento(Enum):
    Débito = 1
    Crédito = 2
    Pix = 3

class Pagamento:
    def __init__(self, valor, data_pagamento, tipo_pagamento):
        self.__valor = valor
        self.__data_pagamento = data_pagamento
        self.__tipo_pagamento = tipo_pagamento

    @property
    def valor(self) -> float:
        return self.__valor
    
    @valor.setter
    def valor(self, valor: float):
        if isinstance(valor, (int, float)):
            self.__valor = valor

    @property
    def data_pagamento(self) -> datetime:
        return self.__data_pagamento
    
    @data_pagamento.setter
    def data_pagamento(self, data_pagamento: datetime):
        if isinstance(data_pagamento, datetime):
            self.__data_pagamento = data_pagamento
  
    @property
    def tipo_pagamento(self) -> TipoPagamento:
        return self.__tipo_pagamento
    
    @tipo_pagamento.setter
    def tipo_pagamento(self, tipo_pagamento: TipoPagamento):
        if isinstance(tipo_pagamento, TipoPagamento):
            self.__tipo_pagamento = tipo_pagamento