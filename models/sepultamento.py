from datetime import datetime
from models.tumulo import Tumulo
from models.falecido import Falecido
from models.concessao import *


class Sepultamento:

    def __init__(
        self,
        cpf_falecido: str,
        nome_falecido: str,
        data_nascimento: datetime,
        data_falecimento: datetime,
        causa_morte: str,
        tumulo: int,
        #tumulo: Tumulo,
        valor: float,
        data_pagamento: datetime,
        tipo_pagamento,
        responsavel,
        responsavel2,
        data_inicio_cons: datetime,
        data_final_cons: datetime,
        status: StatusConcessao,
        data_sepultamento: datetime,
        observacoes: str,
    ):

        self.__falecido = Falecido(
            nome_falecido,
            cpf_falecido,
            data_nascimento,
            data_falecimento,
            causa_morte
        )

        self.tumulo = tumulo

        self.__concessao = Concessao(
            valor,
            data_pagamento,
            tipo_pagamento,
            responsavel,
            responsavel2,
            data_inicio_cons,
            data_final_cons,
            status
        )

        self.data_sepultamento = (
            data_sepultamento
        )

        self.observacoes = observacoes

        self.__ativo = True

    @property
    def falecido(self):
        return self.__falecido

    @property
    def concessao(self):
        return self.__concessao

    @property
    def tumulo(self):
        return self.__tumulo

    @tumulo.setter
    def tumulo(self, tumulo):
       # if not isinstance(
        #    tumulo,Tumulo):
           # raise TypeError("tumulo deve ser Tumulo")
        self.__tumulo = tumulo

    @property
    def data_sepultamento(self):
        return self.__data_sepultamento

    @data_sepultamento.setter
    def data_sepultamento(self, data):

        if not isinstance(data, datetime):
            raise TypeError(
                "data_sepultamento deve ser datetime")
        self.__data_sepultamento = data

    @property
    def observacoes(self):
        return self.__observacoes

    @observacoes.setter
    def observacoes(self, obs):
        if not isinstance(obs, str):
            raise TypeError("observacoesdeve ser string")
        self.__observacoes = obs

    @property
    def ativo(self):
        return self.__ativo

    @ativo.setter
    def ativo(self, ativo):
        if not isinstance(ativo,bool):
            raise TypeError("ativo deve ser bool")
        self.__ativo = ativo

    def encerrar_sepultamento(self):
        self.__ativo = False
