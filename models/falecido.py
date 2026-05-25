import re
from datetime import datetime
from utils.funcoesAuxiliares import validar_cpf


class Falecido:
    def __init__(
        self,
        nome: str,
        cpf: str,
        data_nascimento: datetime,
        data_falecimento: datetime,
        causa_morte: str
    ):
        if not (isinstance(cpf, str) and validar_cpf(cpf)):
            raise ValueError("CPF inválido")
        self.nome = nome
        self.__cpf = re.sub(r'\D', '', cpf)
        self.data_nascimento = data_nascimento
        self.data_falecimento = data_falecimento
        self.causa_morte = causa_morte

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser string")
        if not nome.strip():
            raise ValueError("nome inválido")
        self.__nome = nome


    @property
    def cpf(self) -> str:
        c = self.__cpf 
        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data):
        if not isinstance(data, datetime):
            raise TypeError(
                "data_nascimento deve ser datetime")
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
    def causa_morte(self, causa):
        if not isinstance(
            causa, str):
            raise TypeError("causa_morte deve ser string")
        if not causa.strip():
            raise ValueError("causa_morte inválida")
        self.__causa_morte = causa
