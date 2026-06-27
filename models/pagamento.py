from datetime import datetime
from enum import Enum
from models.database import Database

class TipoPagamento(Enum):
    Débito = 1
    Crédito = 2
    Pix = 3

class Pagamento:
    def __init__(self, valor: float, data_pagamento, tipo_pagamento):
        self.__valor = valor
        self.__data_pagamento = data_pagamento
        self.__tipo_pagamento = tipo_pagamento

#properties
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

#persistência
    def cadastrar(self):
        db     = Database.get_instance()
        cursor = db.coneccao.cursor()
        cursor.execute("""
            INSERT INTO pagamentos (valor, data_pagamento, tipo_pagamento)
            VALUES (?, ?, ?)
        """, (
            self.__valor,
            self.__data_pagamento.strftime("%Y-%m-%d"),
            self.__tipo_pagamento.value
        ))
        db.coneccao.commit()
        self.__id = cursor.lastrowid

    def alterar(self):
        db = Database.get_instance()
        db.coneccao.execute("""
            UPDATE pagamentos
            SET valor = ?, data_pagamento = ?, tipo_pagamento = ?
            WHERE id = ?
        """, (
            self.__valor,
            self.__data_pagamento.strftime("%Y-%m-%d"),
            self.__tipo_pagamento.value,
            self.__id
        ))
        db.coneccao.commit()

    def deletar(self):
        db = Database.get_instance()
        db.coneccao.execute(
            "DELETE FROM pagamentos WHERE id = ?", (self.__id,)
        )
        db.coneccao.commit()
        self.__id = None

#buscar
    @staticmethod
    def buscar_por_id(id: int):
        db  = Database.get_instance()
        row = db.coneccao.execute(
            "SELECT * FROM pagamentos WHERE id = ?", (id,)
        ).fetchone()
        return Pagamento._row_para_objeto(row) if row else None
    
#auxiliar
    @staticmethod
    def _row_para_objeto(row):
        from datetime import datetime
        return Pagamento(
            id = row["id"],
            valor = row["valor"],
            data_pagamento = datetime.strptime(row["data_pagamento"], "%Y-%m-%d"),
            tipo_pagamento = row["tipo_pagamento"]
        )