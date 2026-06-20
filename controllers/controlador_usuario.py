from __future__ import annotations
from typing import TYPE_CHECKING

from models.usuario import Cargo, Usuario
from views.tela_usuario import TelaUsuario

if TYPE_CHECKING:
    from controllers.controlador_geral import ControladorGeral

class ControladorUsuario:
    def __init__(self, controlador_geral: "ControladorGeral"):
        self.__controlador_geral = controlador_geral
        self.__tela_usuario = None
        self.__garantir_admin()

    def __garantir_admin(self):
        if not Usuario.buscar_por_cpf("00000000000"):
            admin = Usuario(
                nome  = "Administrador",
                cargo = Cargo.Gestor,
                email = "admin@eterna.com",
                cpf   = "000.000.000-00",
                senha = "admin123"
            )
            admin.cadastrar()

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

#metodos principais
    def buscar_por_cpf(self, cpf: str):
        return Usuario.buscar_por_cpf(self.__normalizar_cpf(cpf))
    
    def buscar_por_email(self, email: str):
        if not isinstance(email, str):
            return None
        return Usuario.buscar_por_email(email.strip().lower())

    def buscar_por_nome(self, nome: str) -> list:
        if not isinstance(nome, str):
            return []
        return Usuario.buscar_por_nome(nome.strip().lower())

    def buscar_por_cargo(self, cargo: Cargo) -> list:
        if not isinstance(cargo, Cargo):
            return []
        return Usuario.buscar_por_cargo(cargo)

    def listar_usuarios(self) -> list:
        return [u for u in Usuario.buscar_todos() if not self.__is_usuario_mestre(u)]

    def cadastrar_usuario_dados(self, nome, cargo, email, cpf, senha, confirmar_senha) -> Usuario:
        if senha != confirmar_senha:
            raise ValueError("As senhas não conferem.")
        if self.buscar_por_email(email):
            raise ValueError("Já existe usuário com esse email.")
        if self.buscar_por_cpf(cpf):
            raise ValueError("Já existe usuário com esse CPF.")

        usuario = Usuario(nome, cargo, email, cpf, senha)
        usuario.cadastrar()
        return usuario

    def alterar_usuario_dados(self, cpf, nome, cargo, email, senha=None, confirmar_senha=None) -> Usuario:
        usuario = self.buscar_por_cpf(cpf)
        if not usuario:
            raise ValueError("Usuário não encontrado.")
        if self.__is_usuario_mestre(usuario):
            raise ValueError("Usuário mestre não pode ser alterado.")

        outro = self.buscar_por_email(email)
        if outro and outro.cpf != usuario.cpf:
            raise ValueError("Já existe usuário com esse email.")

        if senha is not None or confirmar_senha is not None:
            if senha != confirmar_senha:
                raise ValueError("As senhas não conferem.")
            usuario.alterar_dados(nome, cargo, email, senha)
        else:
            usuario.alterar_dados(nome, cargo, email)

        usuario.alterar()
        return usuario

    def excluir_usuario_por_cpf(self, cpf: str) -> Usuario:
        if self.__normalizar_cpf(cpf) == "00000000000":
            raise ValueError("Usuário mestre não pode ser excluído.")

        usuario = self.buscar_por_cpf(cpf)
        if not usuario:
            raise ValueError("Usuário não encontrado.")

        autenticacao = getattr(self.__controlador_geral, "controlador_autenticacao", None)
        if autenticacao and usuario is autenticacao.usuario_logado:
            raise ValueError("Não é possível excluir o usuário logado.")

        usuario.deletar()
        return usuario

#operações tela
    def abre_tela(self):
        if not self.__controlador_geral:
            raise RuntimeError("Controlador geral não configurado.")
        if not self.__tela_usuario:
            self.__tela_usuario = TelaUsuario(self.__controlador_geral.tela_menu.root)

        while True:
            opcao = self.__tela_usuario.tela_opcoes()
            if   opcao == 0: break
            elif opcao == 1: self.cadastrar_usuario_ui()
            elif opcao == 2: self.alterar_usuario_ui()
            elif opcao == 3: self.excluir_usuario_ui()
            elif opcao == 4: self.listar_usuarios_ui()
            elif opcao == 5: self.buscar_usuario_ui()
            else: self.__tela_usuario.mostra_mensagem("Opção inválida.")

    def cadastrar_usuario_ui(self):
        dados = self.__tela_usuario.pega_dados_cadastro()
        if not dados:
            return
        try:
            cargo = self.__parse_cargo(dados["cargo"])
            self.cadastrar_usuario_dados(
                dados["nome"], cargo, dados["email"],
                dados["cpf"], dados["senha"], dados["senha"]
            )
            self.__tela_usuario.mostra_mensagem("Usuário cadastrado com sucesso.")
        except ValueError as e:
            self.__tela_usuario.mostra_mensagem(str(e))

    def alterar_usuario_ui(self):
        dados = self.__tela_usuario.pega_dados_alteracao()
        if not dados:
            return
        usuario = self.buscar_por_cpf(dados["cpf"])
        if not usuario:
            self.__tela_usuario.mostra_mensagem("Usuário não encontrado.")
            return
        try:
            cargo  = self.__parse_cargo(dados["cargo"]) if dados["cargo"] else usuario.cargo
            senha  = dados["senha"] or None
            self.alterar_usuario_dados(
                dados["cpf"],
                dados["nome"]  or usuario.nome,
                cargo,
                dados["email"] or usuario.email,
                senha, senha
            )
            self.__tela_usuario.mostra_mensagem("Usuário alterado com sucesso.")
        except ValueError as e:
            self.__tela_usuario.mostra_mensagem(str(e))

    def excluir_usuario_ui(self):
        cpf = self.__tela_usuario.pega_dados_exclusao()
        if not cpf:
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
        for u in usuarios:
            texto += (
                f"Nome: {u.nome}\nCPF: {u.cpf}\n"
                f"Email: {u.email}\nCargo: {u.cargo.name}\n\n"
            )
        self.__tela_usuario.mostra_mensagem(texto.strip())

    def buscar_usuario_ui(self):
        cpf = self.__tela_usuario.pega_dados_busca()
        if not cpf:
            return
        usuario = self.buscar_por_cpf(cpf)
        if not usuario:
            self.__tela_usuario.mostra_mensagem("Usuário não encontrado.")
            return
        self.__tela_usuario.mostra_mensagem(
            f"Nome: {usuario.nome}\nCPF: {usuario.cpf}\n"
            f"Email: {usuario.email}\nCargo: {usuario.cargo.name}"
        )