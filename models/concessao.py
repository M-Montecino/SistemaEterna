from datetime import datetime
from enum import Enum
from models.pagamento import Pagamento, TipoPagamento
from models.responsavel import Responsavel 

class StatusConcessao(Enum):
    Ativa = 1
    Carencia = 2
    Vencida = 3

class Concessao:
    def __init__(self, valor, data_pagamento, tipo_pagamento, responsavel, responsavel2, data_inicio, data_fim, status):
        self.pagamento = Pagamento(valor, data_pagamento, tipo_pagamento)
        self.__responsavel = responsavel
        self.__responsavel2 = responsavel2
        self.__data_inicio = data_inicio
        self.__data_fim = data_fim
        self.__status = status

        @property
        def responsavel(self) -> Responsavel:
            return self.__responsavel
        
        @responsavel.setter
        def responsavel(self, responsavel: Responsavel):
            if isinstance(responsavel, Responsavel):
                self.__responsavel = responsavel

        @property
        def responsavel2(self) -> Responsavel:
            return self.__responsavel2
        
        @responsavel2.setter
        def responsavel2(self, responsavel2: Responsavel):
            if isinstance(responsavel2, Responsavel):
                self.__responsavel2 = responsavel2

        @property
        def data_inicio(self) -> datetime:
            return self.__data_inicio
        
        @data_inicio.setter
        def data_inicio(self, data_inicio: datetime):
            if isinstance(data_inicio, datetime):
                self.__data_inicio = data_inicio

        @property
        def data_fim(self) -> datetime:
            return self.__data_fim

        @data_fim.setter
        def data_fim(self, data_fim: datetime):
            if isinstance(data_fim, datetime):
                self.__data_fim = data_fim

        @property
        def status(self) -> StatusConcessao:
            return self.__status

        @status.setter
        def status(self, status: StatusConcessao):
            if isinstance(status, StatusConcessao):
                self.__status = status