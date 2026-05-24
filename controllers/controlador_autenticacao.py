from __future__ import annotations
import hashlib
from typing import TYPE_CHECKING
from models.usuario import Cargo, Usuario
from views.tela_login import TelaLogin

if TYPE_CHECKING:
    from controllers.controlador_usuario import ControladorUsuario


class ControladorAutenticacao:
    def __init__(self, controlador_usuario: ControladorUsuario):
        self.__controlador_usuario = controlador_usuario
        self.__tela_login = TelaLogin()
        self.__usuario_logado = None

    def __normalizar_cpf(self, cpf: str) -> str:
        if not isinstance(cpf, str):
            return ""
        return "".join(caractere for caractere in cpf if caractere.isdigit())

    def __cpf_valido_para_login(self, cpf: str) -> bool:
        return len(self.__normalizar_cpf(cpf)) == 11

    def __verificar_senha(self, usuario: Usuario, senha: str) -> bool:
        if usuario is None or not isinstance(senha, str):
            return False

        try:
            salt_hex, hash_hex = usuario.senha.split("$")
        except ValueError:
            return False

        salt = bytes.fromhex(salt_hex)
        senha_hash = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            salt,
            Usuario.ITERACOES_HASH
        )
        return senha_hash.hex() == hash_hex

    def autenticar(self, cpf: str, senha: str) -> str:
        if not self.__cpf_valido_para_login(cpf):
            return "cpf_invalido"

        usuario = self.__controlador_usuario.buscar_por_cpf(cpf)
        if usuario is None:
            return "cpf_invalido"

        if not self.__verificar_senha(usuario, senha):
            return "senha_invalida"

        self.__usuario_logado = usuario
        return "sucesso"

    def iniciar(self):
        if self.__tela_login is None:
            raise RuntimeError("Tela de login não disponível.")

        while True:
            opcao = self.__tela_login.tela_login()
            if opcao == 0:
                self.__tela_login.mostra_mensagem("Execução cancelada.")
                exit(0)

            dados = self.__tela_login.pega_dados_login()
            cpf = dados.get("cpf", "")
            senha = dados.get("senha", "")

            resultado = self.autenticar(cpf, senha)
            if resultado == "cpf_invalido":
                self.__tela_login.mostra_mensagem(
                    "CPF inválido. Tente novamente."
                )
                continue

            if resultado == "senha_invalida":
                self.__tela_login.mostra_mensagem(
                    "Senha inválida. Tente novamente."
                )
                continue

            self.__tela_login.mostra_mensagem("Login efetuado com sucesso!")
            self.__tela_login.root.withdraw()
            break

    def eh_admin(self) -> bool:
        return self.__usuario_logado is not None and self.__usuario_logado.cargo == Cargo.Gestor

    def logout(self):
        self.__usuario_logado = None

    @property
    def usuario_logado(self):
        return self.__usuario_logado
