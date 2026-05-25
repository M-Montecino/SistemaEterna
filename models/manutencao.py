from datetime import datetime
from enum import Enum
from models.tumulo import Tumulo

class TipoServico(Enum):
    LIMPEZA = 1
    REPARO = 2
    OUTRO = 3

class Manutencao:
    def __init__(self, codigo, tumulo, tipo_servico, data, cpf_responsavel):
        self.__codigo = codigo
        self.__tumulo = tumulo
        self.__tipo_servico = tipo_servico
        self.__data = data
        self.__cpf_responsavel = cpf_responsavel

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def tumulo(self) -> Tumulo:
        return self.__tumulo

    @tumulo.setter
    def tumulo (self, tumulo):
        self.__tumulo = tumulo
    #def tumulo(self, tumulo: Tumulo):
     #   if isinstance(tumulo, Tumulo):
       #     self.__tumulo = tumulo
       # else:
        #    raise ValueError("Tipo de túmulo inválido")

    @property
    def tipo_servico(self) -> TipoServico:
        return self.__tipo_servico

    @tipo_servico.setter
    def tipo_servico(self, tipo_servico: TipoServico):
        if isinstance(tipo_servico, TipoServico):
            self.__tipo_servico = tipo_servico
        else:
            raise ValueError("Tipo de serviço inválido")

    @property
    def data(self) -> datetime:
        return self.__data

    @data.setter
    def data(self, data: datetime):
        if isinstance(data, datetime):
            self.__data = data
        else:
            raise ValueError("Tipo de data inválida")

    @property
    def cpf_responsavel(self) -> str:
        return self.__cpf_responsavel

    @cpf_responsavel.setter
    def cpf_responsavel(self, cpf_responsavel: str):
        if isinstance(cpf_responsavel, str):
            self.__cpf_responsavel = cpf_responsavel
        else:
            raise ValueError("Tipo de cpf inválido")