from datetime import datetime
from models.sepultamento import Sepultamento


class Exumacao:

    def __init__(self,
                 codigo: int,
                 data: datetime,
                 sepultamento: Sepultamento,
                 destino: str,
                 observacoes: str = ""):
        self.__codigo = codigo
        self.__data = data
        self.__sepultamento = sepultamento
        self.__destino = destino
        self.__observacoes = observacoes

    def __validar_codigo(self, codigo: int) -> int:
        if not isinstance(codigo, int):
            raise ValueError("Codigo da exumacao deve ser inteiro.")
        if codigo <= 0:
            raise ValueError("Codigo da exumacao deve ser positivo.")
        return codigo

    def __validar_data(self, data: datetime) -> datetime:
        if not isinstance(data, datetime):
            raise ValueError("Data da exumacao invalida.")
        return data

    def __validar_destino(self, destino: str) -> str:
        if not isinstance(destino, str) or destino.strip() == "":
            raise ValueError("Destino invalido.")
        return destino.strip()

    @property
    def codigo(self) -> int:
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo: int):
        self.__codigo = self.__validar_codigo(codigo)

    @property
    def data(self) -> datetime:
        return self.__data

    @data.setter
    def data(self, data: datetime):
        self.__data = self.__validar_data(data)

    @property
    def sepultamento(self) -> Sepultamento:
        return self.__sepultamento

    @sepultamento.setter
    def sepultamento(self, sepultamento: Sepultamento):
        if not isinstance(sepultamento, Sepultamento):
            raise ValueError("Sepultamento invalido.")
        self.__sepultamento = sepultamento

    @property
    def destino(self) -> str:
        return self.__destino

    @destino.setter
    def destino(self, destino: str):
        self.__destino = self.__validar_destino(destino)

    @property
    def observacoes(self) -> str:
        return self.__observacoes

    @observacoes.setter
    def observacoes(self, observacoes: str):
        if observacoes is None:
            observacoes = ""
        else:
            self.__observacoes = str(observacoes).strip()
