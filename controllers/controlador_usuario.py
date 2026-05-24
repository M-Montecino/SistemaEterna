from __future__ import annotations

from typing import TYPE_CHECKING

from models.usuario import Cargo, Usuario
from views.tela_usuario import TelaUsuario

if TYPE_CHECKING:
    from controllers.controlador_geral import ControladorGeral

class ControladorUsuario:
    def __init__(self, controlador_geral: ControladorGeral):
        self.__controlador_geral = controlador_geral
        self.__usuarios = [
            Usuario(
                "Administrador",
                Cargo.Gestor,
                "admin@eterna.com",
                "000.000.000-00",
                "admin123"
            )
        ]
        self.__tela_usuario = None

    def __normalizar_cpf(self, cpf: str) -> str:
        if not isinstance(cpf, str):
            return ""
        return "".join(caractere for caractere in cpf if caractere.isdigit())

    def __is_usuario_mestre(self, usuario: Usuario) -> bool:
        return usuario is not None and usuario.cpf == "00000000000"

    def __parse_cargo(self, valor: str) -> Cargo:
        if not isinstance(valor, str) or valor.strip() == "":
            raise ValueError("Cargo inválido.")

        if valor.strip() == "1":
            return Cargo.Gestor
        if valor.strip() == "2":
            return Cargo.Secretario

        raise ValueError("Cargo inválido. Digite 1 para Gestor ou 2 para Secretário.")

    def buscar_por_cpf(self, cpf: str):
        cpf = self.__normalizar_cpf(cpf)

        for usuario in self.__usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def buscar_por_email(self, email: str):
        if not isinstance(email, str):
            return None
        email = email.strip().lower()

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
        if not isinstance(cargo, Cargo):
            return []

        return [usuario for usuario in self.__usuarios if usuario.cargo == cargo]

    def listar_usuarios(self) -> list:
        return [usuario for usuario in self.__usuarios if not self.__is_usuario_mestre(usuario)]

    def abre_tela(self):
        if self.__controlador_geral is None:
            raise RuntimeError("Controlador geral não configurado.")

        if self.__tela_usuario is None:
            self.__tela_usuario = TelaUsuario(self.__controlador_geral.tela_menu.root)

        while True:
            opcao = self.__tela_usuario.tela_opcoes()
            if opcao == 0:
                break
            if opcao == 1:
                self.cadastrar_usuario_ui()
            elif opcao == 2:
                self.alterar_usuario_ui()
            elif opcao == 3:
                self.excluir_usuario_ui()
            elif opcao == 4:
                self.listar_usuarios_ui()
            elif opcao == 5:
                self.buscar_usuario_ui()
            else:
                self.__tela_usuario.mostra_mensagem("Opção inválida.")

    def cadastrar_usuario_dados(self,
                                nome: str,
                                cargo: Cargo,
                                email: str,
                                cpf: str,
                                senha: str,
                                confirmar_senha: str) -> Usuario:
        if senha != confirmar_senha:
            raise ValueError("As senhas não conferem")

        if self.buscar_por_email(email) is not None:
            raise ValueError("Já existe usuário com esse email.")

        if self.buscar_por_cpf(cpf) is not None:
            raise ValueError("Já existe usuário com esse CPF.")

        usuario = Usuario(nome, cargo, email, cpf, senha)
        self.__usuarios.append(usuario)
        return usuario

    def alterar_usuario_dados(self,
                               cpf: str,
                               nome: str,
                               cargo: Cargo,
                               email: str,
                               senha: str = None,
                               confirmar_senha: str = None) -> Usuario:
        usuario = self.buscar_por_cpf(cpf)
        if usuario is None:
            raise ValueError("Usuário não encontrado")

        if self.__is_usuario_mestre(usuario):
            raise ValueError("Usuário mestre não pode ser alterado.")

        usuario_email = self.buscar_por_email(email)
        if usuario_email is not None and usuario_email is not usuario:
            raise ValueError("Já existe usuário com esse email.")

        if senha is not None or confirmar_senha is not None:
            if senha != confirmar_senha:
                raise ValueError("As senhas não conferem")
            usuario.alterar_dados(nome, cargo, email, senha)
        else:
            usuario.alterar_dados(nome, cargo, email)

        return usuario

    def excluir_usuario_por_cpf(self, cpf: str) -> Usuario:
        if self.__normalizar_cpf(cpf) == "00000000000":
            raise ValueError("Usuário mestre não pode ser excluído.")

        usuario = self.buscar_por_cpf(cpf)
        if usuario is None:
            raise ValueError("Usuário não encontrado")

        autenticacao = None
        if self.__controlador_geral is not None:
            autenticacao = self.__controlador_geral.controlador_autenticacao

        if autenticacao is not None and usuario is autenticacao.usuario_logado:
            raise ValueError("Não é possível excluir o usuário logado.")

        self.__usuarios.remove(usuario)
        return usuario

    def cadastrar_usuario_ui(self):
        dados = self.__tela_usuario.pega_dados_cadastro()
        if dados is None:
            return

        try:
            cargo = self.__parse_cargo(dados["cargo"])
            self.cadastrar_usuario_dados(
                dados["nome"],
                cargo,
                dados["email"],
                dados["cpf"],
                dados["senha"],
                dados["senha"]
            )
            self.__tela_usuario.mostra_mensagem("Usuário cadastrado com sucesso.")
        except ValueError as e:
            self.__tela_usuario.mostra_mensagem(str(e))

    def alterar_usuario_ui(self):
        dados = self.__tela_usuario.pega_dados_alteracao()
        if dados is None:
            return

        usuario = self.buscar_por_cpf(dados["cpf"])
        if usuario is None:
            self.__tela_usuario.mostra_mensagem("Usuário não encontrado.")
            return

        try:
            cargo = usuario.cargo
            if dados["cargo"]:
                cargo = self.__parse_cargo(dados["cargo"])

            senha = dados["senha"] if dados["senha"] else None
            confirmar = dados["senha"] if dados["senha"] else None

            self.alterar_usuario_dados(
                dados["cpf"],
                dados["nome"] or usuario.nome,
                cargo,
                dados["email"] or usuario.email,
                senha,
                confirmar
            )
            self.__tela_usuario.mostra_mensagem("Usuário alterado com sucesso.")
        except ValueError as e:
            self.__tela_usuario.mostra_mensagem(str(e))

    def excluir_usuario_ui(self):
        cpf = self.__tela_usuario.pega_dados_exclusao()
        if cpf is None:
            return

        try:
            self.excluir_usuario_por_cpf(cpf)
            self.__tela_usuario.mostra_mensagem("Usuário excluído com sucesso.")
        except ValueError as e:
            self.__tela_usuario.mostra_mensagem(str(e))

    def listar_usuarios_ui(self):
        usuarios = self.listar_usuarios()
        if not usuarios:
            self.__tela_usuario.mostra_mensagem("Nenhum usuário cadastrado.")
            return

        texto = ""
        for usuario in usuarios:
            texto += (
                f"Nome: {usuario.nome}\n"
                f"CPF: {usuario.cpf}\n"
                f"Email: {usuario.email}\n"
                f"Cargo: {usuario.cargo.name}\n\n"
            )

        self.__tela_usuario.mostra_mensagem(texto.strip())

    def buscar_usuario_ui(self):
        cpf = self.__tela_usuario.pega_dados_busca()
        if cpf is None:
            return

        usuario = self.buscar_por_cpf(cpf)
        if usuario is None:
            self.__tela_usuario.mostra_mensagem("Usuário não encontrado.")
            return

        self.__tela_usuario.mostra_mensagem(
            f"Nome: {usuario.nome}\n"
            f"CPF: {usuario.cpf}\n"
            f"Email: {usuario.email}\n"
            f"Cargo: {usuario.cargo.name}"
        )
