from views.tela_menu import TelaMenu
from controllers.controlador_manutencao import ControladorManutencao
from controllers.controlador_tumulo import ControladorTumulo
from controllers.controlador_falecido import ControladorFalecido
from controllers.controlador_sepultamento import ControladorSepultamento
from controllers.controlador_concessao import ControladorConcessao
from controllers.controlador_responsavel import ControladorResponsavel
from controllers.controlador_usuario import ControladorUsuario
from controllers.controlador_exumacao import ControladorExumacao


class ControladorGeral:
    def __init__(self):
        self.__controlador_manutencao = ControladorManutencao(self)
        self.__controlador_tumulo = ControladorTumulo(self)
        self.__controlador_falecido = ControladorFalecido(self)
        self.__controlador_sepultamento = ControladorSepultamento(self)
        self.__controlador_concessao = ControladorConcessao(self)
        self.__controlador_responsavel = ControladorResponsavel(self)
        self.__controlador_usuario = ControladorUsuario(self)
        self.__controlador_exumacao = ControladorExumacao(self)
        self.__tela_menu = TelaMenu()

    @property
    def controlador_manutencao(self):
        return self.__controlador_manutencao
    
    @property
    def controlador_tumulo(self):
        return self.__controlador_tumulo
    
    @property
    def controlador_falecido(self):
        return self.__controlador_falecido
    
    @property
    def controlador_sepultamento(self):
        return self.__controlador_sepultamento
    
    @property
    def controlador_concessao(self):
        return self.__controlador_concessao
    
    @property
    def controlador_responsavel(self):
        return self.__controlador_responsavel
    
    @property
    def controlador_usuario(self):
        return self.__controlador_usuario
    
    @property
    def controlador_exumacao(self):
        return self.__controlador_exumacao

    @property
    def tela_menu(self):
        return self.__tela_menu

    def inicializa_sistema(self):
        self.abre_tela()

    def abre_manutencao(self):
        self.__controlador_manutencao.abre_tela()

    def abre_tumulo(self):
        self.__controlador_tumulo.abre_tela()

    def abre_falecido(self):
        self.__controlador_falecido.abre_tela()

    def abre_sepultamento(self):
        self.__controlador_sepultamento.abre_tela()

    def abre_concessao(self):
        self.__controlador_concessao.abre_tela()

    def abre_responsavel(self):
        self.__controlador_responsavel.abre_tela()

    def abre_usuario(self):
        self.__controlador_usuario.abre_tela()

    def abre_exumacao(self):
        self.__controlador_exumacao.abre_tela()

    def encerra_sistema(self):
        self.__tela_menu.mostra_mensagem("Programa falhou com sucesso!")
        exit(0)

    def abre_tela(self):
        lista_opcoes = {
            1: self.abre_manutencao,
            2: self.abre_tumulo,
            3: self.abre_falecido,
            4: self.abre_sepultamento,
            5: self.abre_concessao,
            6: self.abre_responsavel,
            7: self.abre_usuario,
            8: self.abre_exumacao,
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
