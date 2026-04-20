from enum import Enum
import hashlib
import secrets


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


# Classe auxiliar placeholder, futuramente sera substituida por um controler de usuário
class GerenciamentoUsuario:
    def __init__(self):
        self.__usuarios = []
        
    def __normalizar_cpf(self, cpf: str) -> str:
        if not isinstance(cpf, str):
            raise ValueError("CPF invalido")

        cpf_limpo = ""
        for caractere in cpf:
            if caractere.isdigit():
                cpf_limpo += caractere

        if len(cpf_limpo) != 11:
            raise ValueError("CPF invalido")

        return cpf_limpo

    def __normalizar_email(self, email: str) -> str:
        if not isinstance(email, str):
            raise ValueError("Email invalido")

        email = email.strip().lower()

        if email == "":
            raise ValueError("Email invalido")

        return email

    def cadastrar_usuario(self,
                          nome: str,
                          cargo: Cargo,
                          email: str,
                          cpf: str,
                          senha: str,
                          confirmar_senha: str) -> Usuario:
        if senha != confirmar_senha:
            raise ValueError("As senhas nao conferem")

        if self.buscar_por_email(email) is not None:
            raise ValueError("Ja existe usuario com este email")

        if self.buscar_por_cpf(cpf) is not None:
            raise ValueError("Ja existe usuario com este CPF")

        usuario = Usuario(nome, cargo, email, cpf, senha)
        self.__usuarios.append(usuario)
        return usuario

    def listar_usuarios(self) -> list:
        return self.__usuarios.copy()

    def buscar_por_cpf(self, cpf: str):
        cpf = self.__normalizar_cpf(cpf)
        
        for usuario in self.__usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def buscar_por_email(self, email: str):
        email = self.__normalizar_email(email)
        
        for usuario in self.__usuarios:
            if usuario.email == email:
                return usuario
        return None

    def buscar_por_nome(self, nome: str) -> list:
        resultado = []

        if not isinstance(nome, str):
            return resultado

        nome = nome.strip().lower()
        for usuario in self.__usuarios:
            if nome in usuario.nome.lower():
                resultado.append(usuario)

        return resultado

    def buscar_por_cargo(self, cargo: Cargo) -> list:
        resultado = []

        for usuario in self.__usuarios:
            if usuario.cargo == cargo:
                resultado.append(usuario)

        return resultado

    def alterar_usuario(self,
                        cpf: str,
                        nome: str,
                        cargo: Cargo,
                        email: str,
                        senha: str = None,
                        confirmar_senha: str = None) -> Usuario:
        usuario = self.buscar_por_cpf(cpf)

        if usuario is None:
            raise ValueError("Usuario nao encontrado")

        usuario_email = self.buscar_por_email(email)
        if usuario_email is not None and usuario_email != usuario:
            raise ValueError("Ja existe usuario com este email")

        if senha is None and confirmar_senha is None:
            usuario.alterar_dados(nome, cargo, email)
            return usuario

        if senha is None or confirmar_senha is None:
            raise ValueError("Informe a senha e a confirmacao da senha")

        if senha != confirmar_senha:
            raise ValueError("As senhas nao conferem")

        usuario.alterar_dados(nome, cargo, email, senha)
        return usuario

    def excluir_usuario(self, cpf: str) -> Usuario:
        usuario = self.buscar_por_cpf(cpf)

        if usuario is None:
            raise ValueError("Usuario nao encontrado")

        self.__usuarios.remove(usuario)
        return usuario
