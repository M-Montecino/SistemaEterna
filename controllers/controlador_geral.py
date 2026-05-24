from views.tela_menu import TelaMenu

from controllers.controlador_usuario import ControladorUsuario
from controllers.controlador_autenticacao import ControladorAutenticacao
from controllers.controlador_manutencao import ControladorManutencao
from controllers.controlador_tumulo import ControladorTumulo
from controllers.controlador_sepultamento import ControladorSepultamento
from controllers.controlador_responsavel import ControladorResponsavel
from controllers.controlador_exumacao import ControladorExumacao

class ControladorGeral:
    def __init__(self):
        self.__controlador_manutencao = None
        self.__controlador_tumulo = None
        self.__controlador_sepultamento = None
        self.__controlador_responsavel = None
        self.__controlador_usuario = None
        self.__controlador_autenticacao = None
        self.__controlador_exumacao = None
        self.__tela_menu = None

    @property
    def controlador_manutencao(self):
        return self.__controlador_manutencao
    
    @property
    def controlador_tumulo(self):
        return self.__controlador_tumulo
    
    @property
    def controlador_sepultamento(self):
        return self.__controlador_sepultamento
    
    @property
    def controlador_responsavel(self):
        return self.__controlador_responsavel
    
    @property
    def controlador_usuario(self):
        return self.__controlador_usuario
    
    @property
    def controlador_autenticacao(self):
        return self.__controlador_autenticacao
    
    @property
    def controlador_exumacao(self):
        return self.__controlador_exumacao

    @property
    def tela_menu(self):
        return self.__tela_menu

    def inicializa_sistema(self):
        if self.__controlador_usuario is None:
            self.__controlador_usuario = ControladorUsuario(self)

        if self.__controlador_autenticacao is None:
            self.__controlador_autenticacao = ControladorAutenticacao(
                self.__controlador_usuario
            )

        self.__controlador_autenticacao.iniciar()
        self.__tela_menu = TelaMenu()
        self.abre_tela()

    def abre_manutencao(self):
        if self.controlador_manutencao is None:
            self.__controlador_manutencao = ControladorManutencao(self)
        self.__controlador_manutencao.abre_tela()

    def abre_tumulo(self):
        if self.__controlador_tumulo is None:
            self.__controlador_tumulo = ControladorTumulo(self)
        self.__controlador_tumulo.abre_tela()

    def abre_sepultamento(self):
        if self.__controlador_sepultamento is None:
            self.__controlador_sepultamento = ControladorSepultamento(self)
        self.__controlador_sepultamento.abre_tela()

    def abre_responsavel(self):
        if self.__controlador_responsavel is None:
            self.__controlador_responsavel = ControladorResponsavel(self)
        self.__controlador_responsavel.abre_tela()

    def abre_usuario(self):
        if self.__controlador_usuario is None:
            self.__controlador_usuario = ControladorUsuario(self)

        if self.__controlador_autenticacao is None:
            self.__controlador_autenticacao = ControladorAutenticacao(
                self.__controlador_usuario
            )

        if not self.__controlador_autenticacao.eh_admin():
            self.__tela_menu.mostra_mensagem(
                "Acesso negado: apenas administradores podem gerenciar usuários."
            )
            return

        self.__controlador_usuario.abre_tela()

    def abre_exumacao(self):
        if self.__controlador_exumacao is None:
            self.__controlador_exumacao = ControladorExumacao(self)
        self.__controlador_exumacao.abre_tela()

    def logout(self):
        if self.__controlador_autenticacao is not None:
            self.__controlador_autenticacao.logout()

        if self.__tela_menu is not None:
            self.__tela_menu.root.destroy()
            self.__tela_menu = None

        self.__controlador_autenticacao.iniciar()
        self.__tela_menu = TelaMenu()

    def encerra_sistema(self):
        if self.__tela_menu is not None:
            self.__tela_menu.mostra_mensagem("Programa falhou com sucesso!")
        exit(0)

    def abre_tela(self):
        lista_opcoes = {
            1: self.abre_manutencao,
            2: self.abre_tumulo,
            3: self.abre_sepultamento,
            4: self.abre_responsavel,
            5: self.abre_usuario,
            6: self.abre_exumacao,
            7: self.logout,
            0: self.encerra_sistema
        }

        while True:
            try:
                opcao_escolhida = self.__tela_menu.tela_opcoes()
                funcao_escolhida = lista_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    self.__tela_menu.mostra_mensagem(
                        "Opção inválida. Tente novamente.")
            except Exception as e:
                self.__tela_menu.mostra_mensagem(
                    f"Comando inesperado: {str(e)}")
