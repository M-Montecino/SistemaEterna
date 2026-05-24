from views.tela_menu import TelaMenu

class ControladorGeral:
    def __init__(self):
        self.__controlador_manutencao = None
        self.__controlador_tumulo = None
        self.__controlador_sepultamento = None
        self.__controlador_responsavel = None
        self.__controlador_usuario = None
        self.__controlador_exumacao = None
        self.__tela_menu = TelaMenu()

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
    def controlador_exumacao(self):
        return self.__controlador_exumacao

    @property
    def tela_menu(self):
        return self.__tela_menu

    def inicializa_sistema(self):
        self.abre_tela()

    def abre_manutencao(self):
        if self.controlador_manutencao is None:
            try:
                from controllers.controlador_manutencao import ControladorManutencao
                self.__controlador_manutencao = ControladorManutencao(self)
            except ModuleNotFoundError:
                self.__tela_menu.mostra_mensagem(
                    "Função Manutenção ainda não está implementada."
                )
                return
        self.__controlador_manutencao.abre_tela()

    def abre_tumulo(self):
        if self.__controlador_tumulo is None:
            try:
                from controllers.controlador_tumulo import ControladorTumulo
                self.__controlador_tumulo = ControladorTumulo(self)
            except ModuleNotFoundError:
                self.__tela_menu.mostra_mensagem(
                    "Função Túmulo ainda não está implementada."
                )
                return
        self.__controlador_tumulo.abre_tela()

    def abre_sepultamento(self):
        if self.__controlador_sepultamento is None:
            try:
                from controllers.controlador_sepultamento import ControladorSepultamento
                self.__controlador_sepultamento = ControladorSepultamento(self)
            except ModuleNotFoundError:
                self.__tela_menu.mostra_mensagem(
                    "Função Sepultamento ainda não está implementada."
                )
                return
        self.__controlador_sepultamento.abre_tela()

    def abre_responsavel(self):
        if self.__controlador_responsavel is None:
            try:
                from controllers.controlador_responsavel import ControladorResponsavel
                self.__controlador_responsavel = ControladorResponsavel(self)
            except ModuleNotFoundError:
                self.__tela_menu.mostra_mensagem(
                    "Função Responsável ainda não está implementada."
                )
                return
        self.__controlador_responsavel.abre_tela()

    def abre_usuario(self):
        if self.__controlador_usuario is None:
            try:
                from controllers.controlador_usuario import ControladorUsuario
                self.__controlador_usuario = ControladorUsuario(self)
            except ModuleNotFoundError:
                self.__tela_menu.mostra_mensagem(
                    "Função Usuário ainda não está implementada."
                )
                return
        self.__controlador_usuario.abre_tela()

    def abre_exumacao(self):
        if self.__controlador_exumacao is None:
            try:
                from controllers.controlador_exumacao import ControladorExumacao
                self.__controlador_exumacao = ControladorExumacao(self)
            except ModuleNotFoundError:
                self.__tela_menu.mostra_mensagem(
                    "Função Exumação ainda não está implementada."
                )
                return
        self.__controlador_exumacao.abre_tela()

    def encerra_sistema(self):
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
