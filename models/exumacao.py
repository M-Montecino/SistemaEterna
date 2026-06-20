from datetime import datetime
from models.database import Database

class Exumacao:
    def __init__(self,
                 codigo: int,
                 data: datetime,
                 sepultamento: int,
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
    def sepultamento(self) -> int:
        return self.__sepultamento

    @sepultamento.setter
    def sepultamento(self, sepultamento: int):
        if not isinstance(sepultamento, int):
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

#persistência
    def cadastrar(self):
        db = Database.get_instance()
        cursor = db.coneccao.cursor()
        
        cursor.execute("""
            INSERT INTO exumacoes (codigo, data, sepultamento, destino, observacoes)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.__codigo,
            self.__data.strftime("%Y-%m-%d"),
            self.__sepultamento,
            self.__destino,
            self.__observacoes
        ))
        db.coneccao.commit()

    def alterar(self):
        db = Database.get_instance()
        db.coneccao.execute("""
            UPDATE exumacoes
            SET data = ?, sepultamento = ?, destino = ?, observacoes = ?
            WHERE codigo = ?             
        """, (
            self.__data.strftime("%Y-%m-%d"),
            self.__sepultamento,
            self.__destino,
            self.__observacoes,
        ))
        db.coneccao.commit()

    def deletar(self):
        db = Database.get_instance()
        db.coneccao.execute(
            "DELETE FROM exumacoes WHERE codigo = ?", (self.__codigo,)
        )
        db.coneccao.commit()
        self.__codigo = None

#buscas
    @staticmethod
    def buscar_por_codigo(codigo: int):
        db = Database.get_instance()
        row = db.coneccao.execute(
            "SELECT * FROM exumacoes WHERE codigo = ?", (codigo,)
        ).fetchone()
        return Exumacao._row_para_objeto(row) if row else None
    
    @staticmethod
    def buscar_por_cpf_falecido(cpf: str):
        db  = Database.get_instance()
        row = db.coneccao.execute(
            "SELECT * FROM exumacoes WHERE sepultamento = ?", (cpf,)
        ).fetchone()
        return Exumacao._row_para_objeto(row) if row else None
    
    @staticmethod
    def buscar_todos():
        db = Database.get_instance()
        rows = db.coneccao.execute("SELECT * FROM exumacoes").fetchall()
        return [Exumacao._row_para_objeto(r) for r in rows]
    
#auxiliar
    @staticmethod
    def _row_para_objetos(row):
        return Exumacao(
            codigo = row['codigo'],
            data = datetime.strptime(row["data"], "%Y-%m-%d"),
            sepultamento = row['sepultamento'],
            destino= row['destino'],
            observacoes= row['observacoes']
        )