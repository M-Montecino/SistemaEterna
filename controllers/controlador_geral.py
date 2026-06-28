from views.tela_menu import TelaMenu

from models.tumulo import Tumulo
from models.exumacao import Exumacao
from models.usuario import Usuario, Cargo

from controllers.controlador_usuario import ControladorUsuario
from controllers.controlador_autenticacao import ControladorAutenticacao
from controllers.controlador_manutencao import ControladorManutencao
from controllers.controlador_tumulo import ControladorTumulo
from controllers.controlador_sepultamento import ControladorSepultamento
from controllers.controlador_responsavel import ControladorResponsavel
from controllers.controlador_exumacao import ControladorExumacao

class ControladorGeral:
    def __init__(self):
        self.__controlador_usuario = ControladorUsuario(self)
        self.__controlador_autenticacao = ControladorAutenticacao(
            self.__controlador_usuario
        )
        self.__controlador_manutencao = ControladorManutencao(self)
        self.__controlador_tumulo = ControladorTumulo(self)
        self.__controlador_sepultamento = ControladorSepultamento(self)
        self.__controlador_responsavel = ControladorResponsavel(self)
        self.__controlador_exumacao = ControladorExumacao(self)
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
        self.__controlador_autenticacao.iniciar()
        self.__tela_menu = TelaMenu()
        self.abre_tela()

    def abre_manutencao(self):
        self.__controlador_manutencao.abre_tela()

    def abre_tumulo(self):
        self.__controlador_tumulo.abre_tela()

    def abre_sepultamento(self):
        self.__controlador_sepultamento.abre_tela()

    def abre_responsavel(self):
        self.__controlador_responsavel.abre_tela()

    def abre_usuario(self):
        if not self.__controlador_autenticacao.eh_admin():
            self.__tela_menu.mostra_mensagem(
                "Acesso negado: apenas administradores podem gerenciar usuários."
            )
            return

        self.__controlador_usuario.abre_tela()

    def abre_exumacao(self):
        self.__controlador_exumacao.abre_tela()
        
    def __gerar_dados_relatorio_gerencial(self):
        ocupacao_tumulos = Tumulo.buscar_dados_ocupacao()

        total_tumulos_cadastrados = len(ocupacao_tumulos)
        total_tumulos_vazios = 0
        total_tumulos_parcialmente_ocupados = 0
        total_tumulos_lotados = 0

        capacidade_total_cemiterio = 0
        total_vagas_ocupadas = 0
        total_vagas_livres = 0

        for item in ocupacao_tumulos:
            capacidade = item["capacidade"]
            ocupados = item["ocupados"]
            vagas_livres = item["vagas_livres"]

            capacidade_total_cemiterio += capacidade
            total_vagas_ocupadas += ocupados
            total_vagas_livres += vagas_livres

            if ocupados == 0:
                total_tumulos_vazios += 1
            elif ocupados >= capacidade:
                total_tumulos_lotados += 1
            else:
                total_tumulos_parcialmente_ocupados += 1

        exumacoes = Exumacao.buscar_realizadas()

        usuarios = [
            usuario for usuario in Usuario.buscar_todos()
            if usuario.cpf != "00000000000"
        ]

        total_usuarios_gestores = 0
        total_usuarios_secretarios = 0

        for usuario in usuarios:
            if usuario.cargo == Cargo.Gestor:
                total_usuarios_gestores += 1
            elif usuario.cargo == Cargo.Secretario:
                total_usuarios_secretarios += 1

        return {
            "total_tumulos_cadastrados": total_tumulos_cadastrados,
            "total_tumulos_vazios": total_tumulos_vazios,
            "total_tumulos_parcialmente_ocupados": total_tumulos_parcialmente_ocupados,
            "total_tumulos_lotados": total_tumulos_lotados,
            "capacidade_total_cemiterio": capacidade_total_cemiterio,
            "total_vagas_ocupadas": total_vagas_ocupadas,
            "total_vagas_livres": total_vagas_livres,
            "total_sepultamentos_ativos": total_vagas_ocupadas,
            "total_exumacoes_realizadas": len(exumacoes),
            "total_usuarios_gestores": total_usuarios_gestores,
            "total_usuarios_secretarios": total_usuarios_secretarios
        }
        
    def abre_relatorio_gerencial(self):
        if not self.__controlador_autenticacao.eh_admin():
            self.__tela_menu.mostra_mensagem(
                "Acesso negado: apenas gestores podem visualizar o relatório gerencial."
            )
            return

        dados = self.__gerar_dados_relatorio_gerencial()
        self.__tela_menu.mostra_relatorio_gerencial(dados)

    def logout(self):
        if self.__controlador_autenticacao is not None:
            self.__controlador_autenticacao.logout()

        for controlador in (
            self.__controlador_manutencao,
            self.__controlador_tumulo,
            self.__controlador_sepultamento,
            self.__controlador_responsavel,
            self.__controlador_usuario,
            self.__controlador_exumacao,
        ):
            reiniciar = getattr(controlador, "reinicia_tela", None)
            if reiniciar is not None:
                reiniciar()

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
            7: self.abre_relatorio_gerencial,
            8: self.logout,
            0: self.encerra_sistema
        }

        while True:
            try:
                opcao_escolhida = self.__tela_menu.tela_opcoes()
                funcao_escolhida = lista_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    if opcao_escolhida not in (0, 8):
                        self.__tela_menu.root.withdraw()
                        
                    funcao_escolhida()

                    if opcao_escolhida not in (0, 8):
                        self.__tela_menu.root.deiconify()
                else:
                    self.__tela_menu.mostra_mensagem(
                        "Opção inválida. Tente novamente.")
            except Exception as e:
                self.__tela_menu.mostra_mensagem(
                    f"Comando inesperado: {str(e)}")
