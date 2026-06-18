from datetime import datetime
from models.tumulo import Tumulo
from models.falecido import Falecido
from models.concessao import Concessao, StatusConcessao
from models.database import Database

class Sepultamento:
    def __init__(
        self,
        cpf_falecido: str,
        nome_falecido: str,
        data_nascimento: datetime,
        data_falecimento: datetime,
        causa_morte: str,
        tumulo: Tumulo,
        valor: float,
        data_pagamento: datetime,
        tipo_pagamento,
        responsavel,
        responsavel2,
        data_inicio_cons: datetime,
        data_final_cons: datetime,
        status: StatusConcessao,
        data_sepultamento: datetime,
        observacoes: str,
    ):
        self.__falecido = Falecido(
            nome_falecido, cpf_falecido,
            data_nascimento, data_falecimento, causa_morte
        )
        self.__tumulo = tumulo
        self.__concessao = Concessao(
            valor, data_pagamento, tipo_pagamento,
            responsavel, responsavel2,
            data_inicio_cons, data_final_cons, status
        )
        self.__data_sepultamento = data_sepultamento
        self.__observacoes       = observacoes
        self.__ativo             = True

    #properties
    @property
    def falecido(self):
        return self.__falecido

    @property
    def concessao(self):
        return self.__concessao

    @property
    def tumulo(self):
        return self.__tumulo

    @tumulo.setter
    def tumulo(self, tumulo):
        if not isinstance(tumulo, Tumulo):
            raise TypeError("tumulo deve ser Tumulo")
        self.__tumulo = tumulo

    @property
    def data_sepultamento(self):
        return self.__data_sepultamento

    @data_sepultamento.setter
    def data_sepultamento(self, data):
        if not isinstance(data, datetime):
            raise TypeError("data_sepultamento deve ser datetime")
        self.__data_sepultamento = data

    @property
    def observacoes(self):
        return self.__observacoes

    @observacoes.setter
    def observacoes(self, obs):
        if not isinstance(obs, str):
            raise TypeError("observacoes deve ser string")
        self.__observacoes = obs

    @property
    def ativo(self):
        return self.__ativo

    def encerrar_sepultamento(self):
        self.__ativo = False
        self.salvar()

#persistência
    def cadastrar(self):
        self.__falecido.cadastrar()
        self.__concessao.cadastrar()

        db     = Database.get_instance()
        cursor = db.coneccao.cursor()
        cursor.execute("""
            INSERT INTO sepultamentos
                (cpf_falecido, tumulo, id_concessao,
                 data_sepultamento, observacoes, ativo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.__falecido.cpf,
            self.__tumulo.codigo,
            self.__concessao.id,
            self.__data_sepultamento.strftime("%Y-%m-%d"),
            self.__observacoes,
            int(self.__ativo)
        ))
        db.coneccao.commit()

    def alterar(self):
        self.__falecido.alterar()
        self.__concessao.alterar()

        db = Database.get_instance()
        db.coneccao.execute("""
            UPDATE sepultamentos
            SET tumulo = ?, data_sepultamento = ?,
                observacoes = ?, ativo = ?
            WHERE cpf_falecido = ?
        """, (
            self.__tumulo.codigo,
            self.__data_sepultamento.strftime("%Y-%m-%d"),
            self.__observacoes,
            int(self.__ativo),
            self.__falecido.cpf
        ))
        db.coneccao.commit()

    def deletar(self):
        db = Database.get_instance()
        db.coneccao.execute(
            "DELETE FROM sepultamentos WHERE cpf_falecido = ?",
            (self.__falecido.cpf,)
        )
        db.coneccao.commit()
        self.__falecido.deletar()
        self.__concessao.deletar()

#buscas
    @staticmethod
    def buscar_por_cpf(cpf: str):
        db  = Database.get_instance()
        row = db.coneccao.execute(
            "SELECT * FROM sepultamentos WHERE cpf_falecido = ?", (cpf,)
        ).fetchone()
        return Sepultamento._row_para_objeto(row) if row else None

    @staticmethod
    def buscar_todos() -> list:
        db   = Database.get_instance()
        rows = db.coneccao.execute("SELECT * FROM sepultamentos").fetchall()
        return [Sepultamento._row_para_objeto(r) for r in rows]

    @staticmethod
    def buscar_ativos() -> list:
        db   = Database.get_instance()
        rows = db.coneccao.execute(
            "SELECT * FROM sepultamentos WHERE ativo = 1"
        ).fetchall()
        return [Sepultamento._row_para_objeto(r) for r in rows]

    @staticmethod
    def _row_para_objeto(row):
        """Reconstrói o objeto buscando cada filho pelo seu id/cpf."""
        from models.falecido import Falecido
        from models.concessao import Concessao
        from models.tumulo import Tumulo

        falecido  = Falecido.buscar_por_cpf(row["cpf_falecido"])
        concessao = Concessao.buscar_por_id(row["id_concessao"])
        tumulo    = Tumulo.buscar_por_codigo(row["tumulo"])

        sep = Sepultamento(
            cpf_falecido     = falecido.cpf,
            nome_falecido    = falecido.nome,
            data_nascimento  = falecido.data_nascimento,
            data_falecimento = falecido.data_falecimento,
            causa_morte      = falecido.causa_morte,
            tumulo           = tumulo,
            valor            = concessao.pagamento.valor,
            data_pagamento   = concessao.pagamento.data_pagamento,
            tipo_pagamento   = concessao.pagamento.tipo_pagamento,
            responsavel      = concessao.responsavel,
            responsavel2     = concessao.responsavel2,
            data_inicio_cons = concessao.data_inicio,
            data_final_cons  = concessao.data_fim,
            status           = concessao.status,
            data_sepultamento= datetime.strptime(row["data_sepultamento"], "%Y-%m-%d"),
            observacoes      = row["observacoes"] or ""
        )
        sep._Sepultamento__ativo = bool(row["ativo"])
        return sep