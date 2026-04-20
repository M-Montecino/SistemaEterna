from enum import Enum

class TipoTumulo(Enum):
    Cova = 1
    Cripta = 2
    Gaveteiro = 3

class Tumulo:
    def __init__(self,
            codigo,
            setor: str,
            numero: int,
            tipo: TipoTumulo,
            capacidade: int,
        ):

        if not isinstance(codigo, int) or codigo < 0:
            raise ValueError("Código deve ser um inteiro")

        self.__codigo = codigo
        self.setor = setor
        self.numero = numero
        self.tipo = tipo
        self.capacidade = capacidade
        self.lotado = False

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def setor(self) -> str:
        return self.__setor

    @setor.setter
    def setor(self, setor: str):
        if isinstance(setor, str):
            self.__setor = setor.strip().upper()
        else:
            raise ValueError("Tipo de setor inválido")

    @property
    def numero(self) -> int:
        return self.__numero

    @numero.setter
    def numero(self, numero: int):
        if isinstance(numero, int) and numero >= 0:
            self.__numero = numero
        else:
            raise ValueError("Tipo de número inválido")

    @property
    def tipo(self) -> TipoTumulo:
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo: TipoTumulo):
        if isinstance(tipo, TipoTumulo):
            self.__tipo = tipo
        else:
            raise ValueError("Tipo de tumulo inválido")

    @property
    def capacidade(self) -> int:
        return self.__capacidade

    @capacidade.setter
    def capacidade(self, capacidade: int):
        if isinstance(capacidade, int) and capacidade >= 0:
            self.__capacidade = capacidade
        else:
            raise ValueError("Tipo de capacidade inválido")

    @property
    def lotado(self) -> bool:
        return self.__lotado

    @lotado.setter
    def lotado(self, lotado: bool):
        if isinstance(lotado, bool):
            self.__lotado = lotado
        else:
            raise ValueError("Tipo de lotado inválido")
