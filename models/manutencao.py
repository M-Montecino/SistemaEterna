from datetime import datetime
from enum import Enum
from models.database import Database

class TipoServico(Enum):
    LIMPEZA = 1
    REPARO = 2
    OUTRO = 3

class Manutencao:
    def __init__(self, codigo, tumulo, tipo_servico, data, cpf_responsavel):
        self.__codigo = codigo
        self.__tumulo = tumulo
        self.__tipo_servico = tipo_servico
        self.__data = data
        self.__cpf_responsavel = cpf_responsavel

#properties

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def tumulo(self) -> int:
        return self.__tumulo

    @tumulo.setter
    def tumulo(self, tumulo: int):
       if isinstance(tumulo, int):
           self.__tumulo = tumulo
       else:
           raise ValueError("Tipo de túmulo inválido")

    @property
    def tipo_servico(self) -> TipoServico:
        return self.__tipo_servico

    @tipo_servico.setter
    def tipo_servico(self, tipo_servico: TipoServico):
        if isinstance(tipo_servico, TipoServico):
            self.__tipo_servico = tipo_servico
        else:
            raise ValueError("Tipo de serviço inválido")

    @property
    def data(self) -> datetime:
        return self.__data

    @data.setter
    def data(self, data: datetime):
        if isinstance(data, datetime):
            self.__data = data
        else:
            raise ValueError("Tipo de data inválida")

    @property
    def cpf_responsavel(self) -> str:
        return self.__cpf_responsavel

    @cpf_responsavel.setter
    def cpf_responsavel(self, cpf_responsavel: str):
        if isinstance(cpf_responsavel, str):
            self.__cpf_responsavel = cpf_responsavel
        else:
            raise ValueError("Tipo de cpf inválido")
        
#persisência
    def cadastrar(self):
        db = Database.get_instance()
        cursor = db.coneccao.cursor()
        tipo = self.__tipo_servico.name
        data = self.__data.strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO manutencoes (codigo, tumulo, tipo_servico, data, cpf_responsavel)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.__codigo,
            self.__tumulo, 
            tipo, 
            data, 
            self.__cpf_responsavel
            ))
        db.coneccao.commit()

    def alterar(self):
        db = Database.get_instance()
        cursor = db.coneccao.cursor()

        tipo = self.__tipo_servico.name
        data = self.__data.strftime("%Y-%m-%d")

        cursor.execute("""
            UPDATE manutencoes
            SET tumulo = ?, tipo_servico = ?, data = ?, cpf_responsavel = ?
            WHERE codigo = ?
            """, (
                self.__tumulo,
                tipo, 
                data, 
                self.__cpf_responsavel, 
                self.__codigo
            ))
        db.coneccao.commit()

    def deletar(self):
        db = Database.get_instance()
        db.coneccao.execute(
            "DELETE FROM manutencoes WHERE codigo = ?", (self.__codigo,)
        )
        db.coneccao.commit()
        self.__codigo = None

#buscas
    @staticmethod
    def buscar_por_codigo(codigo: int):
        db  = Database.get_instance()
        row = db.coneccao.execute(
            "SELECT * FROM manutencoes WHERE codigo = ?", (codigo,)
        ).fetchone()
        return Manutencao._row_para_objeto(row) if row else None
    
    @staticmethod
    def buscar_todos():
        db = Database.get_instance()
        rows = db.coneccao.execute("SELECT * FROM manutencoes").fetchall()
        return [Manutencao._row_para_objeto(r) for r in rows]

#auxiliar
    @staticmethod
    def _row_para_objeto(row):
        return Manutencao(
            codigo = row["codigo"],
            tumulo = row["tumulo"],
            tipo_servico = TipoServico[row["tipo_servico"]],
            data = datetime.strptime(row["data"], "%Y-%m-%d"),
            cpf_responsavel = row["cpf_responsavel"]
        )