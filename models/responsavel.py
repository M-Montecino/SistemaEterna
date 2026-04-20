from utils.funcoesAuxiliares import validar_cpf, validar_email

class Responsavel:
    __responsaveis = []

    def __init__(self,
        nome: str,
        cpf: str,
        telefone: str,
        cep: str,
        numero: int,
        email: str
    ) -> None:
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.cep = cep
        self.numero = numero
        self.email = email

        Responsavel.__responsaveis.append(self)


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
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str) -> None:
        if isinstance(cpf, str) and validar_cpf(cpf):
            self.__cpf = cpf
        else:
            raise ValueError("CPF inválido")

    @property
    def telefone(self) -> str:
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone: str) -> None:
        if isinstance(telefone, str):
            self.__telefone = telefone
        else:
            raise ValueError("Tipo de telefone inválido")

    @property
    def cep(self) -> str:
        return self.__cep

    @cep.setter
    def cep(self, cep: str) -> None:
        if isinstance(cep, str):
            self.__cep = cep
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

    @classmethod
    def listar_responsaveis(cls):
        return cls.__responsaveis

    @classmethod
    def remover_responsavel(cls, responsavel):
        if responsavel in cls.__responsaveis:
            cls.__responsaveis.remove(responsavel)
        else:
            raise ValueError("Responsável não encontrado")

    @classmethod
    def limpar_lista_testes(cls):
        cls.__responsaveis.clear()