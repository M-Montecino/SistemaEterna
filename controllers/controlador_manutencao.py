from models.manutencao import Manutencao, TipoServico
from views.tela_manutencao import TelaManutencao
from utils.funcoesAuxiliares import validar_cpf
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controllers.controlador_geral import ControladorGeral

class ControladorManutencao:
    def __init__(self, controlador_geral: "ControladorGeral"):
        self.__controlador_geral = controlador_geral
        self.__tela_manutencao = TelaManutencao(controlador_geral.tela_menu.root)

    #Funções auxiliares
    def __validar_codigo(self, codigo):
        if not isinstance(codigo, int):
            raise ValueError("O código deve ser um inteiro.")

        if codigo <= 0:
            raise ValueError("O código deve ser positivo.")

        if codigo > 999999:
            raise ValueError("Código muito grande.")

    def __converter_tipo_servico(self, tipo_servico):
        if isinstance(tipo_servico, TipoServico):
            return tipo_servico
        if isinstance(tipo_servico, str):
            texto = tipo_servico.strip()
            if texto.isdigit():
                try:
                    return TipoServico(int(texto))
                except ValueError:
                    pass
            try:
                return TipoServico[texto.upper()]
            except KeyError:
                raise ValueError("Tipo de serviço inválido.")
        if isinstance(tipo_servico, int):
            try:
                return TipoServico(tipo_servico)
            except ValueError:
                pass
        raise ValueError("Tipo de serviço inválido.")

    def __validar_data(self, data: datetime):
        if not isinstance(data, datetime):
            raise ValueError("Data inválida.")
        
    def __validar_dados_manutencao(self, dados):
        self.__validar_codigo(dados['codigo'])
        dados['tipo_servico'] = self.__converter_tipo_servico(dados['tipo_servico'])
        self.__controlador_geral.controlador_tumulo.__validar_tumulo(dados['tumulo'])
        self.__validar_data(dados['data'])
        if not validar_cpf(dados['cpf_responsavel']):
            raise ValueError("CPF do responsável inválido.")

    def __formatar_manutencao(self, manutencao):
        return {
            "Código:": manutencao.codigo,
            "Túmulo:": manutencao.tumulo,
            "Tipo de Serviço:": manutencao.tipo_servico,
            "Data:": manutencao.data.strftime("%d/%m/%Y"),
            "CPF do Responsável:": manutencao.cpf_responsavel
        }

    #Funções principais
    def cadastrar_manutencao(self):
        try:
            dados = self.__tela_manutencao.pega_dados_manutencao()
            self.__validar_dados_manutencao(dados)

            if Manutencao.buscar_por_codigo(dados['codigo']):
                self.__tela_manutencao.mostra_mensagem(
                "Código já cadastrado."
                )
                return

            nova = Manutencao(
                dados['codigo'],
                dados['tumulo'],
                dados['tipo_servico'],
                dados['data'],
                dados['cpf_responsavel'] 
            )

            nova.cadastrar()
            self.__tela_manutencao.mostra_mensagem(
                "Manutenção adicionada com sucesso"
            )

        except ValueError as erro:
            self.__tela_manutencao.mostra_mensagem(
                f"Erro ao cadastrar manutenção: {str(erro)}"
            )
        
    def alterar_manutencao(self):
        try:
            codigo = self.__tela_manutencao.alterar_manutencao()
            self.__validar_codigo(codigo)

            manutencao = Manutencao.buscar_por_codigo(codigo)
            if not manutencao:
                self.__tela_manutencao.mostra_mensagem(
                    "Manutenção não encontrada."
                    )
                return
            
            novos_dados = (
            self.__tela_manutencao.pega_novos_dados_manutencao()
            )

            dados_finais = {
            'codigo': codigo,
            'tumulo': novos_dados['tumulo'] if novos_dados['tumulo'] is not None else manutencao.tumulo,
            'tipo_servico': novos_dados['tipo_servico'] if novos_dados['tipo_servico'] is not None else manutencao.tipo_servico,
            'data': novos_dados['data'] if novos_dados['data'] is not None else manutencao.data,
            'cpf_responsavel': novos_dados['cpf_responsavel'] if novos_dados['cpf_responsavel'] is not None else manutencao.cpf_responsavel
            }

            self.__validar_dados_manutencao(dados_finais)

            #atualizando dados
            manutencao.tumulo = dados_finais['tumulo']
            manutencao.tipo_servico = dados_finais['tipo_servico']
            manutencao.data = dados_finais['data']
            manutencao.cpf_responsavel = dados_finais['cpf_responsavel']

            manutencao.alterar()            
            self.__tela_manutencao.mostra_mensagem(
                "Manutenção alterada com sucesso."
            )

        except ValueError as erro:
            self.__tela_manutencao.mostra_mensagem(
                f"Erro ao alterar manutenção: {str(erro)}"
            )           
    
    def excluir_manutencao(self):
        try:
            codigo = self.__tela_manutencao.excluir_manutencao()
            self.__validar_codigo(codigo)

            manutencao = Manutencao.buscar_por_codigo(codigo)
            if not manutencao:
                self.__tela_manutencao.mostra_mensagem("Manutenção não encontrada.")
                return
            
            manutencao.deletar()
            self.__tela_manutencao.mostra_mensagem("Manutenção excluída com sucesso.")

        except ValueError as erro:
            self.__tela_manutencao.mostra_mensagem(
                f"Erro ao cadastrar manutenção: {str(erro)}"
            )

    def listar_manutencoes(self):
        manutencoes = Manutencao.buscar_todos()

        if not manutencoes:
            self.__tela_manutencao.mostra_mensagem(
            "Nenhuma manutenção cadastrada")
            return
        
        for manutencao in manutencoes:
            self.__tela_manutencao.mostra_mensagem(
                self.__formatar_manutencao(manutencao)
            )

    def buscar_manutencao(self):
        try:
            codigo = self.__tela_manutencao.buscar_manutencao()
            self.__validar_codigo(codigo)
            
            manutencao = Manutencao.buscar_por_codigo(codigo)
            if manutencao:
                self.__tela_manutencao.mostra_mensagem(
                    self.__formatar_manutencao(manutencao)
                )
            else:
                self.__tela_manutencao.mostra_mensagem(
                    "Manutenção não encontrada"
                )
        except ValueError as erro:
            self.__tela_manutencao.mostra_mensagem(
                f"Erro ao cadastrar manutenção: {str(erro)}"
            )

    def retomar_menu(self):
        return

    def abre_tela(self):
        opcoes = {
            1: self.cadastrar_manutencao,
            2: self.alterar_manutencao,
            3: self.excluir_manutencao,
            4: self.listar_manutencoes,
            5: self.buscar_manutencao,
            0: self.retomar_menu
        }

        while True:
            try:
                opcao = self.__tela_manutencao.tela_opcoes()
                funcao = opcoes.get(opcao)
                if funcao:
                    funcao()
                    if opcao == 0:
                        break
                else:
                    self.__tela_manutencao.mostra_mensagem("Opção inválida.")
            except ValueError as e:
                self.__tela_manutencao.mostra_mensagem(f"Erro: {str(e)}")