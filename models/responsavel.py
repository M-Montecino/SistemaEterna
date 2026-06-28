from utils.funcoesAuxiliares import *
import re
from datetime import datetime
from models.database import Database

class Responsavel:
    def __init__(self,
        nome: str,
        cpf: str,
        telefone: str,
        cep: str,
        numero: int,
        email: str,
        data_nascimento
    ) -> None:
        if not (isinstance(cpf, str) and validar_cpf(cpf)):
            raise ValueError("CPF inválido")

        cpf_limpo = re.sub(r'\D', '', cpf)
        from models.falecido import Falecido
        if Falecido.buscar_por_cpf(cpf_limpo):
            raise ValueError("CPF consta como falecido")

        self.nome = nome
        self.__cpf = cpf_limpo
        self.telefone = telefone
        self.cep = cep
        self.numero = numero
        self.email = email
        self.data_nascimento = data_nascimento

    def __validar_data_nascimento(self, data_nascimento) -> datetime:
        if isinstance(data_nascimento, datetime):
            dt = data_nascimento
        elif isinstance(data_nascimento, str):
            try:
                dt = datetime.strptime(data_nascimento, "%d/%m/%Y")
            except ValueError as exc:
                raise ValueError("Data de nascimento inválida") from exc
        else:
            raise ValueError("Data de nascimento inválida")

        today = datetime.now()
        idade = today.year - dt.year - ((today.month, today.day) < (dt.month, dt.day))
        if idade < 18:
            raise ValueError("O responsável deve ser maior de 18 anos.")

        return dt

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
        c = self.__cpf 
        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"

    @property
    def telefone(self) -> str:
        t = self.__telefone
        return f"{t[:2]} {t[2:7]}-{t[7:]}"

    @telefone.setter
    def telefone(self, telefone: str) -> None:
        if isinstance(telefone, str) and validar_telefone(telefone):
            self.__telefone = re.sub(r'\D', '', telefone)
        else:
            raise ValueError("Tipo de telefone inválido")

    @property
    def cep(self) -> str:
        cep = self.__cep
        return f"{cep[:5]}-{cep[5:]}"


    @cep.setter
    def cep(self, cep: str) -> None:
        if isinstance(cep, str) and validar_cep(cep):
            self.__cep = re.sub(r'\D', '', cep)
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

    @property
    def data_nascimento(self) -> datetime:
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        self.__data_nascimento = self.__validar_data_nascimento(data_nascimento)
        
#persistencia
    def cadastrar(self):
        db = Database.get_instance()
        cursor = db.coneccao.cursor()
        cursor.execute("""
            INSERT INTO responsaveis (cpf, nome, telefone, cep, numero, email, data_nascimento)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.__cpf,
            self.__nome,
            self.__telefone,
            self.__cep,
            self.__numero,
            self.__email,
            self.__data_nascimento.strftime("%Y-%m-%d")
        ))
        db.coneccao.commit()

    def alterar(self):
        db = Database.get_instance()
        cursor = db.coneccao.cursor()

        cursor.execute("""
            UPDATE responsaveis
            SET nome = ?, telefone = ?, cep = ?, numero = ?, email = ?, data_nascimento = ?
            WHERE cpf = ?
        """, (
            self.__nome,
            self.__telefone,
            self.__cep,
            self.__numero,
            self.__email,
            self.__data_nascimento.strftime("%Y-%m-%d"),
            self.__cpf
        ))
        db.coneccao.commit()
    
    def deletar(self):
        db = Database.get_instance()
        db.coneccao.execute(
            "DELETE FROM responsaveis WHERE cpf = ?", (self.__cpf,)
        )
        db.coneccao.commit()
        self.__cpf = None
    
#buscas
    @staticmethod
    def buscar_por_cpf(cpf):
        db = Database.get_instance()
        row = db.coneccao.execute(
            "SELECT * FROM responsaveis WHERE cpf = ?", (re.sub(r'\D', '', cpf),)
        ).fetchone()
        return Responsavel._row_para_objeto(row) if row else None
    
    @staticmethod
    def buscar_todos():
        db = Database.get_instance()
        rows = db.coneccao.execute("SELECT * FROM responsaveis").fetchall()
        return [Responsavel._row_para_objeto(r) for r in rows]

#auxiliar
    @staticmethod
    def _row_para_objeto(row):
        responsavel = object.__new__(Responsavel)
        responsavel._Responsavel__nome = row["nome"]
        responsavel._Responsavel__cpf = row["cpf"]
        responsavel._Responsavel__telefone = row["telefone"]
        responsavel._Responsavel__cep = row["cep"]
        responsavel._Responsavel__numero = row["numero"]
        responsavel._Responsavel__email = row["email"]
        responsavel._Responsavel__data_nascimento = datetime.strptime(row["data_nascimento"], "%Y-%m-%d")
        return responsavel
