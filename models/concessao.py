from datetime import datetime
from enum import Enum
from models.pagamento import Pagamento
from models.database import Database

class StatusConcessao(Enum):
    ATIVA = 1
    CARENCIA = 2
    VENCIDA = 3

class Concessao:
    def __init__(self, valor, data_pagamento, tipo_pagamento, responsavel, responsavel2, data_inicio, data_fim, status, 
    id=None):
        self.pagamento = Pagamento(valor, data_pagamento, tipo_pagamento)
        self.__id = id
        self.__responsavel = responsavel
        self.__responsavel2 = responsavel2
        self.__data_inicio = data_inicio
        self.__data_fim = data_fim
        self.__status = status

#properties
    @property
    def id(self):
        return self.__id
    
    @property
    def responsavel(self) -> str:
        return self.__responsavel
    
    @responsavel.setter
    def responsavel(self, responsavel: str):
        if isinstance(responsavel, str):
            self.__responsavel = responsavel

    @property
    def responsavel2(self) -> str:
        return self.__responsavel2
    
    @responsavel2.setter
    def responsavel2(self, responsavel2: str):
        if isinstance(responsavel2, str):
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

#persistência
    def cadastrar(self):
        #cadastra pagamento
        self.pagamento.cadastrar()

        db = Database.get_instance()
        cursor = db.coneccao.cursor()
        id_pagamento = cursor.execute("""
                SELECT MAX(id) as id
                FROM pagamentos
            """).fetchone()["id"]
        print("id_pagamento:", id_pagamento)
        print("responsavel:", self.__responsavel)
        print("responsavel2:", self.__responsavel2)

        print(cursor.execute(
            "SELECT * FROM pagamentos WHERE id = ?",
            (id_pagamento,)
        ).fetchone())

        print(cursor.execute(
            "SELECT * FROM responsaveis WHERE cpf = ?",
            (self.__responsavel,)
        ).fetchone())

        print(cursor.execute(
            "SELECT * FROM responsaveis WHERE cpf = ?",
            (self.__responsavel2,)
        ).fetchone())
        cursor.execute("""
            INSERT INTO concessoes
                (id_pagamento, responsavel, responsavel2, data_inicio, data_fim, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            id_pagamento,               
            self.__responsavel,
            self.__responsavel2,
            self.__data_inicio.strftime("%Y-%m-%d"),
            self.__data_fim.strftime("%Y-%m-%d"),
            self.__status.name
        ))
        db.coneccao.commit()
        self.__id = cursor.lastrowid

    def alterar(self):
        self.pagamento.alterar()
        db = Database.get_instance()

        db.coneccao.execute("""
            UPDATE concessoes
            SET responsavel = ?, responsavel2 = ?,
                data_inicio = ?, data_fim = ?, status = ?
            WHERE id = ?
        """, (
            self.__responsavel,
            self.__responsavel2,
            self.__data_inicio.strftime("%Y-%m-%d"),
            self.__data_fim.strftime("%Y-%m-%d"),
            self.__status.name,
            self.__id
        ))
        db.coneccao.commit()

    def deletar(self):
        db = Database.get_instance()
        db.coneccao.execute(
            "DELETE FROM concessoes WHERE id = ?", (self.__id,)
        )
        db.coneccao.commit()
        self.pagamento.deletar()                      

#buscas
    @staticmethod
    def buscar_por_id(id: int):
        db  = Database.get_instance()
        row = db.coneccao.execute(
            "SELECT * FROM concessoes WHERE id = ?", (id,)
        ).fetchone()
        return Concessao._row_para_objeto(row) if row else None

    @staticmethod
    def buscar_todos() -> list:
        db   = Database.get_instance()
        rows = db.coneccao.execute("SELECT * FROM concessoes").fetchall()
        return [Concessao._row_para_objeto(r) for r in rows]

#auxiliar
    @staticmethod
    def _row_para_objeto(row):
        pagamento = Pagamento.buscar_por_id(row["id_pagamento"])

        return Concessao(
            id = row["id"],
            valor = pagamento.valor,
            data_pagamento = pagamento.data_pagamento,
            tipo_pagamento = pagamento.tipo_pagamento,
            responsavel = row["responsavel"],     
            responsavel2 = row["responsavel2"],
            data_inicio = datetime.strptime(row["data_inicio"], "%Y-%m-%d"),
            data_fim = datetime.strptime(row["data_fim"],    "%Y-%m-%d"),
            status = StatusConcessao[row["status"]]
        )
    @staticmethod
    def possui_concessao_vencida(cpf):
        db = Database.get_instance()

        row = db.coneccao.execute("""
            SELECT 1
            FROM concessoes
            WHERE (responsavel = ? OR responsavel2 = ?)
            AND status = 'VENCIDA'
            LIMIT 1
        """, (cpf, cpf)).fetchone()

        return row is not None