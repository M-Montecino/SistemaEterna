from enum import Enum
import hashlib
import secrets
from models.database import Database

class Cargo(Enum):
    Gestor = 1
    Secretario = 2


class Usuario:
    ITERACOES_HASH = 100000

    def __init__(self,
                 nome: str,
                 cargo: Cargo,
                 email: str,
                 cpf: str,
                 senha: str):
        self.nome = nome
        self.cargo = cargo
        self.email = email
        self.__cpf = self.__validar_cpf(cpf)
        self.senha = senha

    def __validar_cpf(self, cpf: str) -> str:
        if not isinstance(cpf, str):
            raise ValueError("CPF invalido")

        cpf_limpo = ""
        for caractere in cpf:
            if caractere.isdigit():
                cpf_limpo += caractere

        if len(cpf_limpo) != 11:
            raise ValueError("CPF invalido")

        return cpf_limpo

    def __validar_email(self, email: str) -> str:
        if not isinstance(email, str):
            raise ValueError("Email invalido")

        email = email.strip().lower()
        if email == "" or "@" not in email or "." not in email or " " in email:
            raise ValueError("Email invalido")

        return email

    def __validar_nome(self, nome: str) -> str:
        if not isinstance(nome, str) or nome.strip() == "":
            raise ValueError("Nome invalido")

        return nome.strip()

    def __validar_senha(self, senha: str) -> str:
        if not isinstance(senha, str) or len(senha.strip()) < 4:
            raise ValueError("Senha invalida")

        return senha.strip()

    def __proteger_senha(self, senha: str) -> str:
        senha = self.__validar_senha(senha)
        salt = secrets.token_bytes(16)
        senha_hash = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            salt,
            Usuario.ITERACOES_HASH
        )
        return f"{salt.hex()}${senha_hash.hex()}"

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = self.__validar_nome(nome)

    @property
    def cargo(self) -> Cargo:
        return self.__cargo

    @cargo.setter
    def cargo(self, cargo: Cargo):
        if isinstance(cargo, Cargo):
            self.__cargo = cargo
        else:
            raise ValueError("Cargo invalido")

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str):
        self.__email = self.__validar_email(email)

    @property
    def cpf(self) -> str:
        return self.__cpf

    @property
    def senha(self) -> str:
        return self.__senha

    @senha.setter
    def senha(self, senha: str):
        self.__senha = self.__proteger_senha(senha)

    def alterar_dados(self,
                      nome: str,
                      cargo: Cargo,
                      email: str,
                      senha: str = None):
        self.nome = nome
        self.cargo = cargo
        self.email = email

        if senha is not None and senha.strip() != "":
            self.senha = senha

#persistência
    def cadastrar(self):
        db = Database()
        cursor = db.coneccao.cursor()
        cursor.execute("""
            INSERT INTO usuarios (cpf, nome, cargo, email, senha_hash)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.__cpf,
            self.__nome,
            self.__cargo.name,
            self.__email,
            self.__senha
        ))
        db.coneccao.commit()

    def alterar(self):
        db = Database().get_instance()
        cursor = db.coneccao.cursor()

        cursor.execute("""
            UPDATE usuarios
            SET nome = ?, cargo = ?, email = ?, senha_hash
            WHERE cpf = ?
        """, (
            self.__nome,
            self.__cargo.name,
            self.__email,
            self.__senha,
            self.__cpf
        ))
        db.coneccao.commit()

    def deletar(self):
        db = Database.get_instance()
        db.coneccao.execute(
            "DELETE FROM usuarios WHERE cpf = ?"
        )
        db.coneccao.commit()
        self.__codigo = None

#buscas
    @staticmethod
    def buscar_por_cpf(cpf):
        db = Database.get_instance()
        row = db.coneccao.execute(
            "SELECT * FROM usuarios WHERE cpf = ?"
        ).fetchone()
        return Usuario._row_para_objeto(row) if row else None

    @staticmethod
    def buscar_todos():
        db = Database.get_instance()
        rows = db.coneccao.execute("SELECT * FROM usuarios").fetchall()
        return [Usuario.row_para_objeto(r) for r in rows]
    
#auxiliar
    def _row_para_objeto(row):
        return Usuario(
            nome = row["nome"],
            cargo = Cargo[row["cargo"]],
            email = row["cargo"],
            senha = row["senha_hash"],
            cpf = row["cpf"]
        )