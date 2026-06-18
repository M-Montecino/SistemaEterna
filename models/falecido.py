import re
from datetime import datetime
from utils.funcoesAuxiliares import validar_cpf
from models.database import Database

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
        self.__nome = nome
        self.__cpf = re.sub(r'\D', '', cpf)
        self.__data_nascimento = data_nascimento
        self.__data_falecimento = data_falecimento
        self.__causa_morte = causa_morte

#properties

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

#persistência
    def cadastrar(self):
        db = Database.get_instance()
        cursor = db.coneccao.cursor()
        cursor.execute("""
            INSERT INTO falecidos (cpf, nome, data_nascimento, data_falecimento, causa_morte)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.__cpf,
            self.__nome,
            self.__data_nascimento.strftime("%Y-%m-%d"),
            self.__data_falecimento.strftime("%Y-%m-%d"),
            self.__causa_morte
            ))
        db.connecao.commit()

    def alterar(self):
        db = Database.get_instance()
        cursor = db.coneccao.cursor()

        cursor.execute("""
            UPDATE falecidos
            SET nome = ?, data_nascimento = ?, data_falecimento = ?, causa_morte = ?
            WHERE cpf = ?
            """, (
                self.__nome,
                self.__data_falecimento.strftime("%Y-%m-%d"),
                self.__data_falecimento.strftime("%Y-%m-%d"),
                self.__causa_morte
            ))
        db.coneccao.commit()

    def deletar(self):
        db = Database.get_instance()
        db.coneccao.execute(
            "DELETE FROM falecidos WHERE cpf = ?", (self.__cpf,)
        )
        db.coneccao.commit()
        self.__cpf = None

#buscas
    @staticmethod
    def buscar_por_codigo(cpf: int):
        db = Database.get_instance()
        row = db.coneccao.execute(
            "SELECT * FROM falecidos WHERE cpf = ?", (cpf)
        ).fetchone()
        return Falecido._row_para_objeto(row) if row else None
    
    @staticmethod
    def buscar_todos():
        db = Database.get_instance()
        rows = db.coneccao.execute("SELECT * FROM falecidos").fetchall()
        return [Falecido._row_para_objeto(r) for r in rows]
    
#auxiliar
    @staticmethod
    def _row_para_objeto(row):
        return Falecido(
            nome= row['nome'],
            cpf= row['cpf'],
            data_nascimento=datetime.strptime(row["data_nascimento"], "%Y-%m-%d"),
            data_falecimento=datetime.strptime(row["data_falecimento"], "%Y-%m-%d"),
            causa_morte= row['causa_morte']
        )