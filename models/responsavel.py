from utils.funcoesAuxiliares import *
import re

class Responsavel:

    def __init__(self,
        nome: str,
        cpf: str,
        telefone: str,
        cep: str,
        numero: int,
        email: str
    ) -> None:
        if not (isinstance(cpf, str) and validar_cpf(cpf)):
            raise ValueError("CPF inválido")

        self.nome = nome
        self.__cpf = re.sub(r'\D', '', cpf)
        self.telefone = telefone
        self.cep = cep
        self.numero = numero
        self.email = email


    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        if isinstance(nome, str) and nome.strip():
            self.__nome = nome.strip()
        else:
            raise ValueError("Tipo ou valor de nome inválido")

    @property
    def cpf(self) -> str:
        c = self.__cpf 
        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"

    @property
    def telefone(self) -> str:
        t = self.__telefone
        return f"{t[:2]} {t[2:7]}-{t[7:]}"

    @telefone.setter
    def telefone(self, telefone: str) -> None:
        if isinstance(telefone, str) and validar_telefone(telefone):
            self.__telefone = re.sub(r'\D', '', telefone)
        else:
            raise ValueError("Tipo de telefone inválido")

    @property
    def cep(self) -> str:
        cep = self.__cep
        return f"{cep[:5]}-{cep[5:]}"


    @cep.setter
    def cep(self, cep: str) -> None:
        if isinstance(cep, str) and validar_cep(cep):
            self.__cep = re.sub(r'\D', '', cep)
        else:
            raise ValueError("Tipo de CEP inválido")

    @property
    def numero(self) -> int:
        return self.__numero

    @numero.setter
    def numero(self, numero: int) -> None:
        if isinstance(numero, int) and numero >= 0:
            self.__numero = numero
        else:
            raise ValueError("Tipo de número inválido")

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str) -> None:
        if isinstance(email, str) and validar_email(email):
            self.__email = email
        else:
            raise ValueError("E-mail inválido")
