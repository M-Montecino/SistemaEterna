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

        usuario = self.__controlador_usuario.buscar_por_cpf(cpf)

        if usuario is None:
            self.__tela_login.mostra_mensagem("Usuário não encontrado.")
            return False
        if not self.__verificar_senha(usuario, senha):
            self.__tela_login.mostra_mensagem("Senha incorreta.")
            return False

        self.__usuario_logado = usuario
        
        self.__tela_login.mostra_mensagem(f"Bem-vindo, {usuario.nome}!")
        return True

    def iniciar(self):
        if self.__tela_login is None:
            raise RuntimeError("Tela de login não disponível.")

        while True:
            opcao = self.__tela_login.tela_login()

            if opcao == 0:
                self.__tela_login.mostra_mensagem("Execução cancelada.")
                exit(0)

            elif opcao == 1:
                dados = self.__tela_login.pega_dados_login()

            cpf = dados.get("cpf", "")
            senha = dados.get("senha", "")

            if self.autenticar(cpf, senha):
                self.__tela_login.root.withdraw()
                break

    def eh_admin(self) -> bool:
        return self.__usuario_logado is not None and self.__usuario_logado.cargo == Cargo.Gestor

    def logout(self):
        self.__usuario_logado = None

    @property
    def usuario_logado(self):
        return self.__usuario_logado
