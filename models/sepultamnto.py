from utils.funcoesAuxiliares import *
import re
from datetime import datetime
from tumulo import Tumulo
from responsavel import Responsavel
from pagamento import TipoPagamento


class Sepultamento:

    def __init__(
        self,
        cpf_falecido: str,
        nome_falecido: str,
        data_nascimento: datetime,
        data_falecimento: datetime,
        causa_morte: str,
        tumulo: Tumulo,
        valor_pagamento: float,
        data_pagamento: datetime,
        tipo_pagamento: TipoPagamento,
        responsavel: Responsavel,
        responsavel2: Responsavel,
        data_inicio_cons: datetime,
        data_final_cons: datetime,
        data_sepultamento: datetime,
        observacoes: str,
    ):

#FALECIDO
        if not (isinstance(cpf_falecido, str) and validar_cpf(cpf_falecido)):
            raise ValueError("CPF inválido")

        self.__cpf_falecido = re.sub(r'\D', '', cpf) = cpf_falecido
        self.nome_falecido = nome_falecido
        self.data_nascimento = data_nascimento
        self.data_falecimento = data_falecimento
        self.causa_morte = causa_morte
        self.tumulo = tumulo
#PAGAMENTO
        self.valor_pagamento = valor_pagamento
        self.data_pagamento = data_pagamento
        self.tipo_pagamento = tipo_pagamento
#RESPONSAVEL
        self.responsavel = responsavel
        self.responsavel2 = responsavel2
#CONCESSAO
        self.data_inicio_cons = data_inicio_cons
        self.data_final_cons = data_final_cons

        self.data_sepultamento = data_sepultamento
        self.observacoes = observacoes
        self.__ativo = True


    @property
    def cpf_falecido(self) -> str:
        c = self.__cpf_falecido 
        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"

    @property
    def nome_falecido(self):
        return self.__nome_falecido

    @nome_falecido.setter
    def nome_falecido(self, nome):
        if not isinstance(nome, str) and nome.strip():
            raise TypeError("nome_falecido deve ser string")
        self.__nome_falecido = nome

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data):
        if not isinstance(data, datetime):
            raise TypeError("data_nascimento deve ser datetime")

        self.__data_nascimento = data

    @property
    def data_falecimento(self):
        return self.__data_falecimento

    @data_falecimento.setter
    def data_falecimento(self, data):

        if not isinstance(data, datetime):
            raise TypeError("data_falecimento deve ser datetime")

        self.__data_falecimento = data

    @property
    def causa_morte(self):
        return self.__causa_morte

    @causa_morte.setter
    def causa_morte(self, morte):
        if not isinstance(morte, str):
            raise TypeError("causa_morte deve ser string")
        self.__causa_morte = morte

    @property
    def tumulo(self):
        return self.__tumulo

    @tumulo.setter
    def tumulo(self, valor):

        if not isinstance(valor, Tumulo):
            raise TypeError("tumulo deve ser um objeto Tumulo")

        self.__tumulo = valor

    @property
    def valor_pagamento(self):
        return self.__valor_pagamento

    @valor_pagamento.setter
    def valor_pagamento(self, valor):
        if not isinstance(valor, (float, int)):
            raise TypeError("valor_pagamento deve ser float")
        self.__valor_pagamento = float(valor)

    @property
    def data_pagamento(self):
        return self.__data_pagamento

    @data_pagamento.setter
    def data_pagamento(self, data):
        if not isinstance(data, datetime):
            raise TypeError("data_pagamento deve ser datetime")
        self.__data_pagamento = data

    @property
    def tipo_pagamento(self):
        return self.__tipo_pagamento

    @tipo_pagamento.setter
    def tipo_pagamento(self, tipo):
        if not isinstance(tipo, TipoPagamento):
            raise TypeError("tipo_pagamento deve ser TipoPagamento")

        self.__tipo_pagamento = tipo

    @property
    def responsavel(self):
        return self.__responsavel

    @responsavel.setter
    def responsavel(self, resp):
        if not isinstance(resp, Responsavel):
            raise TypeError("responsavel deve ser Responsavel")
        self.__responsavel = resp

    @property
    def responsavel2(self):
        return self.__responsavel2

    @responsavel2.setter
    def responsavel2(self, resp):

        if not isinstance(resp, Responsavel):
            raise TypeError("responsavel2 deve ser Responsavel")
        self.__responsavel2 = resp

    @property
    def data_inicio_cons(self):
        return self.__data_inicio_cons

    @data_inicio_cons.setter
    def data_inicio_cons(self, data):
        if not isinstance(data, datetime):
            raise TypeError("data_inicio_cons deve ser datetime")

        self.__data_inicio_cons = data

    @property
    def data_final_cons(self):
        return self.__data_final_cons

    @data_final_cons.setter
    def data_final_cons(self, data):

        if not isinstance(data, datetime):
            raise TypeError("data_final_cons deve ser datetime")
        self.__data_final_cons = data

    @property
    def data_sepultamento(self):
        return self.__data_sepultamento

    @data_sepultamento.setter
    def data_sepultamento(self, data):
        if not isinstance(data, datetime):
            raise TypeError("data_sepultamento deve ser datetime")
        self.__data_sepultamento = data

    @property
    def observacoes(self):
        return self.__observacoes

    @observacoes.setter
    def observacoes(self, obs):
        if not isinstance(obs, str):
            raise TypeError("observacoes deve ser string")
        self.__observacoes = obs

    @property
    def ativo(self):
        return self.__ativo

    @ativo.setter
    def ativo(self, atv):
        if not isinstance(atv, bool):
            raise TypeError("ativo deve ser boolean")
        self.__ativo = atv

    def encerrar_concessao(self):
        self.__ativo = False
