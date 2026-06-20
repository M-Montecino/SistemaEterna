from models.sepultamento import Sepultamento
from models.pagamento import TipoPagamento
from models.concessao import StatusConcessao
from utils.funcoesAuxiliares import validar_cpf, formatar_cpf
from views.tela_sepultamento import TelaSepultamento
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controllers.controlador_geral import ControladorGeral

class ControladorSepultamento:
    def __init__(
        self,
        controlador_geral: "ControladorGeral"):
        self.__controlador_geral = (controlador_geral)
        self.__tela_sepultamento = (
            TelaSepultamento(controlador_geral.tela_menu.root))

#Funções auxiliares
    def __validar_nome(self, nome: str):
        if not nome.strip():
            raise ValueError("Nome não pode ser vazio.")
        if any(char.isdigit() for char in nome):
            raise ValueError("Nome não pode conter números.")
        
    def __validar_texto(self, texto: str):
        if not texto.strip():
            raise ValueError("Este campo não pode estar vazio.")
    
    def __validar_valor_pagamento(self, valor_pagamento):
        if not isinstance(valor_pagamento, (float, int)):
            raise ValueError("Valor de pagamento inválido.")
        if valor_pagamento < 0:
            raise ValueError("Valor de pagamento não pode ser negativo.")
        
    def __converter_tipo_pagamento(self, tipo):
        if isinstance(tipo, TipoPagamento):
            return tipo
        if isinstance(tipo, str):
            texto = tipo.strip()
            if texto.isdigit():
                try:
                    return TipoPagamento(int(texto))
                except ValueError:
                    pass
            try:
                return TipoPagamento[texto.upper()]
            except KeyError:
                raise ValueError("Tipo de pagamento inválido.")
        if isinstance(tipo, int):
            try:
                return TipoPagamento(tipo)
            except ValueError:
                pass
        raise ValueError("Tipo de pagamento inválido.")
    
    def __converter_status_concessao(self, status):
        if isinstance(status, StatusConcessao):
            return status
        if isinstance(status, str):
            texto = status.strip()
            if texto.isdigit():
                try:
                    return StatusConcessao(int(texto))
                except ValueError:
                    pass
            try:
                return StatusConcessao[texto.upper()]
            except KeyError:
                raise ValueError("Status de concessão inválido.")
        if isinstance(status, int):
            try:
                return StatusConcessao(status)
            except ValueError:
                pass
        raise ValueError("Status de concessão inválido.")

    def __validar_data(self, data: datetime):
        if not isinstance(data, datetime):
            raise ValueError("Data inválida.")

    def __validar_dados_sepultamento(self, dados):
        if not validar_cpf(dados['cpf_falecido']):
            raise ValueError("CPF do falecido inválido.")
        self.__validar_nome(dados['nome_falecido'])
        self.__validar_data(dados['data_nascimento'])
        self.__validar_data(dados['data_falecimento'])
        self.__validar_texto(dados['causa_morte'])
        self.__controlador_geral.controlador_tumulo.__validar_tumulo(dados['tumulo'])
        self.__validar_valor_pagamento(dados['valor'])
        self.__validar_data(dados['data_pagamento'])
        dados['tipo_pagamento']  = self.__converter_tipo_pagamento(dados['tipo_pagamento'])
        self.__validar_data(dados['data_inicio_cons'])
        self.__validar_data(dados['data_final_cons'])
        dados['status'] = self.__converter_status_concessao(dados['status'])
        self.__validar_data(dados['data_sepultamento'])
        self.__validar_texto(dados['observacoes'])

        if dados['data_nascimento'] > dados['data_falecimento']:
            raise ValueError("Nascimento não pode ser posterior ao falecimento.")
        if dados['data_inicio_cons'] > dados['data_final_cons']:
            raise ValueError("Início da concessão não pode ser posterior ao fim.")
        if dados['data_sepultamento'] < dados['data_falecimento']:
            raise ValueError("Sepultamento não pode ser anterior ao falecimento.")

    def __formatar_sepultamento(self, s: Sepultamento):
        f = s.falecido
        c = s.concessao
        return {
            "Falecido": f.nome,
            "CPF": f.cpf,
            "Nascimento": f.data_nascimento.strftime("%d/%m/%Y"),
            "Falecimento": f.data_falecimento.strftime("%d/%m/%Y"),
            "Causa da morte": f.causa_morte,
            "Data sepultamento": s.data_sepultamento.strftime("%d/%m/%Y"),
            "Observações": s.observacoes,
            "Valor": c.pagamento.valor,
            "Data pagamento": c.pagamento.data_pagamento.strftime("%d/%m/%Y"),
            "Tipo de pagamento": c.pagamento.tipo_pagamento,
            "Responsável 1": c.responsavel,
            "Responsável 2": c.responsavel2,
            "Início concessão": c.data_inicio.strftime("%d/%m/%Y"),
            "Fim concessão": c.data_fim.strftime("%d/%m/%Y"),
            "Status concessão": c.status.name,
        }
    
    #metodos principais
    def cadastrar_sepultamento(self):
        try:
            dados = self.__tela_sepultamento.pega_dados_sepultamento()
            self.__validar_dados_sepultamento(dados)

            if Sepultamento.buscar_por_cpf(dados['cpf_falecido']):
                self.__tela_sepultamento.mostra_mensagem("CPF já cadastrado.")
                return
            
            novo = Sepultamento(
                dados['cpf_falecido'],
                dados['nome_falecido'],
                dados['data_nascimento'],
                dados['data_falecimento'],
                dados['causa_morte'],

                dados['tumulo'],

                dados['valor'],          
                dados['data_pagamento'],
                dados['tipo_pagamento'], 
                dados['responsavel'],
                dados['responsavel2'],   
                dados['data_inicio_cons'],
                dados['data_final_cons'],
                dados['status'],

                dados['data_sepultamento'], 
                dados['observacoes']
            )

            novo.cadastrar()
            self.__tela_sepultamento.mostra_mensagem(
                "Sepultamento cadastrado com sucesso."
                )
            
        except ValueError as erro:
            self.__tela_sepultamento.mostra_mensagem(
                f"Erro ao cadastrar sepultamento: {str(erro)}"
                )

    def alterar_sepultamento(self):
        try:
            cpf = self.__tela_sepultamento.pega_cpf_alteracao()
            if not validar_cpf(cpf):
                raise ValueError("CPF inválido.")

            sepultamento = Sepultamento.buscar_por_cpf(cpf)
            if not sepultamento:
                self.__tela_sepultamento.mostra_mensagem("Sepultamento não encontrado.")
                return

            novos = self.__tela_sepultamento.pega_novos_dados_sepultamento()
            f = sepultamento.falecido
            c = sepultamento.concessao

            dados_finais = {
                'cpf_falecido': f.cpf,
                'nome_falecido': novos['nome_falecido'] or f.nome,
                'data_nascimento':novos['data_nascimento'] or f.data_nascimento,
                'data_falecimento': novos['data_falecimento'] or f.data_falecimento,
                'causa_morte': novos['causa_morte'] or f.causa_morte,
                'tumulo': novos['tumulo'] or sepultamento.tumulo,
                'valor': novos['valor'] or c.pagamento.valor,
                'data_pagamento': novos['data_pagamento'] or c.pagamento.data_pagamento,
                'tipo_pagamento': novos['tipo_pagamento'] or c.pagamento.tipo_pagamento,
                'responsavel': novos['responsavel'] or c.responsavel,
                'responsavel2': novos['responsavel2'] or c.responsavel2,
                'data_inicio_cons': novos['data_inicio_cons'] or c.data_inicio,
                'data_final_cons': novos['data_final_cons'] or c.data_fim,
                'status': novos['status'] or c.status,
                'data_sepultamento': novos['data_sepultamento'] or sepultamento.data_sepultamento,
                'observacoes': novos['observacoes'] or sepultamento.observacoes,
            }

            self.__validar_dados_sepultamento(dados_finais)

            #atualizando dados
            f.nome = dados_finais['nome_falecido']
            f.data_nascimento = dados_finais['data_nascimento']
            f.data_falecimento = dados_finais['data_falecimento']
            f.causa_morte = dados_finais['causa_morte']
            sepultamento.tumulo = dados_finais['tumulo']
            c.pagamento.valor = dados_finais['valor']
            c.pagamento.data_pagamento = dados_finais['data_pagamento']
            c.pagamento.tipo_pagamento = dados_finais['tipo_pagamento']
            c.responsavel = dados_finais['responsavel']
            c.responsavel2 = dados_finais['responsavel2']
            c.data_inicio  = dados_finais['data_inicio_cons']
            c.data_fim = dados_finais['data_final_cons']
            c.status  = dados_finais['status']
            sepultamento.data_sepultamento = dados_finais['data_sepultamento']
            sepultamento.observacoes = dados_finais['observacoes']


            sepultamento.alterar()
            self.__tela_sepultamento.mostra_mensagem(
                "Sepultamento alterado com sucesso."
                )    
            
        except ValueError as erro:
            self.__tela_sepultamento.mostra_mensagem(
                f"Erro ao alterar sepultamento: {str(erro)}"
            )

    def excluir_sepultamento(self):
        try:
            cpf = self.__tela_sepultamento.pega_cpf_exclusao()
            if not validar_cpf(cpf):
                raise ValueError("CPF inválido.")

            sepultamento = Sepultamento.buscar_por_cpf(cpf)
            if not sepultamento:
                self.__tela_sepultamento.mostra_mensagem("Sepultamento não encontrado.")
                return

            sepultamento.deletar()
            self.__tela_sepultamento.mostra_mensagem("Sepultamento excluído com sucesso.")

        except ValueError as e:
            self.__tela_sepultamento.mostra_mensagem(f"Erro ao excluir: {str(e)}")

    def listar_sepultamentos(self):
        sepultamentos = Sepultamento.buscar_todos()
        if not sepultamentos:
            self.__tela_sepultamento.mostra_mensagem("Nenhum sepultamento cadastrado.")
            return
        for s in sepultamentos:
            self.__tela_sepultamento.mostra_mensagem(self.__formatar_sepultamento(s))

    def buscar_sepultamento(self):
        try:
            cpf = self.__tela_sepultamento.pega_cpf_alteracao()
            if not validar_cpf(cpf):
                raise ValueError("CPF inválido.")

            sepultamento = Sepultamento.buscar_por_cpf(cpf)
            if sepultamento:
                self.__tela_sepultamento.mostra_mensagem(
                    self.__formatar_sepultamento(sepultamento)
                )
            else:
                self.__tela_sepultamento.mostra_mensagem("Sepultamento não encontrado.")

        except ValueError as e:
            self.__tela_sepultamento.mostra_mensagem(f"Erro ao buscar: {str(e)}")


    def retomar_menu(self):
        return

    def abre_tela(self):

        lista_opcoes = {
            1: self.cadastrar_sepultamento,
            2: self.alterar_sepultamento,
            3: self.excluir_sepultamento,
            4: self.listar_sepultamentos,
            5: self.buscar_sepultamento,
            0: self.retomar_menu
        }

        while True:

            try:

                opcao = (self.__tela_sepultamento.tela_opcoes())
                funcao = (lista_opcoes.get(opcao))
                if funcao:
                    funcao()
                    if opcao == 0:
                        break
                else:
                    self.__tela_sepultamento.mostra_mensagem("Opção inválida.")

            except ValueError as erro:
                self.__tela_sepultamento.mostra_mensagem( f"Erro: {str(erro)}")

    def validar_sepultamento(self, cpf):
        if not Sepultamento.buscar_por_cpf(cpf):
            raise ValueError("Esse sepultamento não existe.")