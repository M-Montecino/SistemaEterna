from enum import Enum
from models.database import Database

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

#properties

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

#persistencia
    def cadastrar(self):
        db = Database.get_instance()
        cursor = db.coneccao.cursor()

        cursor.execute("""
            INSERT INTO tumulos (codigo, setor, numero, tipo, capacidade)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.__codigo,
            self.__setor,
            self.__numero,
            self.__tipo.name,
            self.__capacidade
            ))
        db.coneccao.commit()

    def alterar(self):
        db = Database.get_instance()
        cursor = db.coneccao.cursor()

        cursor.execute("""
                UPDATE tumulos
                SET setor = ?, numero = ?, tipo = ?, capacidade = ?
                WHERE codigo = ?
        """, (
            self.__setor,
            self.__numero,
            self.__tipo.name,
            self.__capacidade
        ))
    
    def deletar(self):
        db = Database.get_instance()
        db.coneccao.execute(
            "DELETE FROM tumulos WHERE codigo = ?", (self.__cpf,)
        )
        db.coneccao.commit()
        self.__cpf = None

#buscas
    @staticmethod
    def buscar_por_codigo(codigo):
        db = Database.get_instance()
        row = db.coneccao.execute(
            "SELECT * FROM tumulos WHERE codigo ?", (codigo,)
        ).fetchone()
        return Tumulo.row_para_objeto(row) if row else None
    
    @staticmethod
    def buscar_todos():
        db = Database.get_instance()
        rows = db.coneccao.execute("SELECT * FROM tumulos").fetchall
        return [Tumulo._row_para_objeto(r) for r in rows]
    
#auxiliar
    @staticmethod
    def _row_para_objeto(row):
        return Tumulo(
            codigo = row['codigo'],
            setor = row['setor'],
            numero = row['numero'],
            tipo = TipoTumulo(row['tipo']),
            capacidade = row['capacidade']
        )
