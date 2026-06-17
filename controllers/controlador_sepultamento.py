from models.sepultamento import Sepultamento
from models.pagamento import Pagamento, TipoPagamento
from models.falecido import Falecido
from models.concessao import Concessao, StatusConcessao
from models.tumulo import *
from utils.funcoesAuxiliares import validar_cpf, formatar_cpf
from views.tela_sepultamento import TelaSepultamento

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.controlador_geral import (
        ControladorGeral
    )

class ControladorSepultamento:
    def __init__(
        self,
        controlador_geral: "ControladorGeral"):
        self.__sepultamentos = []
        self.__controlador_geral = (controlador_geral)
        self.__tela_sepultamento = (
            TelaSepultamento(controlador_geral.tela_menu.root))

    #Metodos auxiliares
    def __auxiliar_busca_sepultamento(self, cpf: str):
        cpf_formatado = formatar_cpf(cpf)
        for sep in (self.__sepultamentos):
            if (sep.falecido.cpf == cpf_formatado):
                return sep
        return None

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
        
    def __converter_tipo_pagamento(self, tipo_pagamento):
        if isinstance(tipo_pagamento, TipoPagamento):
            return tipo_pagamento

        if isinstance(tipo_pagamento, str):
            texto = tipo_pagamento.strip()
            if texto.isdigit():
                try:
                    return TipoPagamento(int(texto))
                except ValueError:
                    pass

            texto_normalizado = texto.strip().upper()
            try:
                return TipoPagamento[texto_normalizado]
            except KeyError:
                raise ValueError("Tipo de pagamento inválido.")

        if isinstance(tipo_pagamento, int):
            try:
                return TipoPagamento(tipo_pagamento)
            except ValueError:
                pass

        raise ValueError("Tipo de serviço inválido.")
    
    def __converter_status_concessao(self, status_concessao):
        if isinstance(status_concessao, StatusConcessao):
            return status_concessao

        if isinstance(status_concessao, str):
            texto = status_concessao.strip()
            if texto.isdigit():
                try:
                    return StatusConcessao(int(texto))
                except ValueError:
                    pass

            texto_normalizado = texto.strip().upper()
            try:
                return StatusConcessao[texto_normalizado]
            except KeyError:
                raise ValueError("Tipo de serviço inválido.")

        if isinstance(status_concessao, int):
            try:
                return StatusConcessao(status_concessao)
            except ValueError:
                pass

        raise ValueError("Tipo de serviço inválido.")

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
        dados['tipo_pagamento'] = self.__converter_tipo_pagamento(dados['tipo_pagamento'])
        self.__controlador_geral.controlador_responsavel.__validar_cpf(dados['responsavel'])
        self.__controlador_geral.controlador_responsavel.__validar_cpf(dados['responsavel'])
        self.__validar_data(dados['data_inicio_cons'])
        self.__validar_data(dados['data_final_cons'])
        dados['status'] = self.__converter_status_concessao(dados['status'])
        self.__validar_data(dados['data_sepultamento'])
        self.__validar_texto(dados['observacoes'])

        if dados['data_nascimento'] > dados['data_falecimento']:
            raise ValueError("Data de nascimento não pode ser posterior à data de falecimento.")
        if dados['data_inicio_cons'] > dados['data_final_cons']:
            raise ValueError("Data de início da concessão não pode ser posterior à data final.")
        if dados['data_sepultamento'] < dados['data_falecimento']:
            raise ValueError("Data de sepultamento não pode ser anterior ao falecimento.")

    def __formatar_sepultamento(self, sepultamento: Sepultamento):
        falecido = (sepultamento.falecido)
        concessao = (sepultamento.concessao)
        return {
            "Falecido:":
                falecido.nome,
            "CPF:":
                falecido.cpf,
            "Nascimento:":
                falecido.data_nascimento.strftime("%d/%m/%Y"),
            "Falecimento:":
                falecido.data_falecimento.strftime("%d/%m/%Y"),
            "Causa da morte:":
                falecido.causa_morte,
            "Data Sepultamento:":
                sepultamento.data_sepultamento.strftime("%d/%m/%Y"),
            "Observações:":
                sepultamento.observacoes,
            "Valor:": 
                concessao.pagamento.valor,
            "Data Pagamento:": 
                concessao.pagamento.data_pagamento.strftime("%d/%m/%Y"),
            "Tipo de Pagamento:": 
                concessao.pagamento.tipo_pagamento,
            "Responsável 1:":
                concessao.responsavel,
            "Responsável 2:":
                concessao.responsavel2,
            "Data Início Concessão:":
                concessao.data_inicio.strftime("%d/%m/%Y"),
            "Data Final Concessão:":
                concessao.data_fim.strftime("%d/%m/%Y"),
            "Status Concessão:":    
                concessao.status
            }
    
    #metodos principais
    def cadastrar_sepultamento(self):
        try:
            dados = self.__tela_sepultamento.pega_dados_sepultamento()
            self.__validar_dados_sepultamento(dados)

            if self.__auxiliar_busca_sepultamento(dados['cpf_falecido']):
                self.__tela_sepultamento.mostra_mensagem(
                        "CPF já cadastrado"
                    )
                return

            novo_sepultamento = (Sepultamento(
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
                ))

            self.__sepultamentos.append(novo_sepultamento)
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
            sepultamento = self.__auxiliar_busca_sepultamento(validar_cpf(cpf))
            sepultamento_atualizado = sepultamento

            if not sepultamento:
                self.__tela_sepultamento.mostra_mensagem(
                    "Sepultamento não encontrado."
                    )
                return

            novos_dados = self.__tela_sepultamento.pega_novos_dados_sepultamento()

            #atualizando dados
            if novos_dados['nome_falecido'] is not None:
                sepultamento_atualizado.falecido.nome = novos_dados['nome_falecido']
            if novos_dados['data_nascimento'] is not None:
                sepultamento_atualizado.falecido.data_nascimento = novos_dados['data_nascimento']
            if novos_dados['data_falecimento'] is not None:
                sepultamento_atualizado.falecido.data_falecimento = novos_dados['data_falecimento']
            if novos_dados['causa_morte'] is not None:
                sepultamento_atualizado.falecido.causa_morte = novos_dados['causa_morte']

            if novos_dados['tumulo'] is not None:
               sepultamento_atualizado.tumulo = novos_dados['tumulo']

            if novos_dados['valor'] is not None:
               sepultamento_atualizado.concessao.valor = novos_dados['valor']

            if novos_dados['data_pagamento'] is not None:
               sepultamento_atualizado.concessao.data_pagamento = novos_dados['data_pagamento']
            if novos_dados['tipo_pagamento'] is not None:
               sepultamento_atualizado.concessao.tipo_pagamento = self.__converter_tipo_pagamento(novos_dados['tipo_pagamento'])

            if novos_dados['responsavel'] is not None:
               sepultamento_atualizado.responsavel = novos_dados['responsavel']
            if novos_dados['responsavel2'] is not None:
               sepultamento_atualizado.responsavel2 = novos_dados['responsavel2']

            if novos_dados['data_inicio_cons'] is not None:
               sepultamento_atualizado.concessao.data_inicio_cons = novos_dados['data_inicio_cons']
            if novos_dados['data_final_cons'] is not None:
               sepultamento_atualizado.concessao.data_final_cons = novos_dados['data_final_cons']
            if novos_dados['status'] is not None:
               sepultamento_atualizado.concessao.status = novos_dados['status']

            if novos_dados['data_sepultamento'] is not None:
               sepultamento_atualizado.data_sepultamento = novos_dados['data_sepultamento']
            if novos_dados['observacoes'] is not None:
               sepultamento_atualizado.observacoes = novos_dados['observacoes']

            self.__validar_dados_sepultamento(sepultamento_atualizado)
            sepultamento = sepultamento_atualizado

            self.__tela_sepultamento.mostra_mensagem(
                "Sepultamento alterado com sucesso."
                )    
            
        except ValueError as erro:
            self.__tela_sepultamento.mostra_mensagem(
                f"Erro ao alterar sepultamento: {str(erro)}"
            )

    def excluir_sepultamento(self):
        cpf = self.__tela_sepultamento.pega_cpf_exclusao()
        sepultamento = self.__auxiliar_busca_sepultamento(validar_cpf(cpf))

        if sepultamento:
            self.__sepultamentos.remove(sepultamento)
            self.__tela_sepultamento.mostra_mensagem(
                "Sepultamento excluído com sucesso."
                )
        else:
            self.__tela_sepultamento.mostra_mensagem(
                "Sepultamento não encontrado."
                )

    def listar_sepultamentos(self):
        if not self.__sepultamentos:
            self.__tela_sepultamento.mostra_mensagem(
                "Nenhum sepultamento cadastrado."
                )
            return

        for sepultamento in (self.__sepultamentos):
            self.__tela_sepultamento.mostra_mensagem(
                self.__formatar_sepultamento(sepultamento)
            )

    def buscar_sepultamento(self):
        cpf = self.__tela_sepultamento.pega_cpf_alteracao()
        sepultamento = self.__auxiliar_busca_sepultamento(validar_cpf(cpf))

        if sepultamento:
            self.__tela_sepultamento.mostra_mensagem(
                self.__formatar_sepultamento(sepultamento)
            )
        else:
            self.__tela_sepultamento.mostra_mensagem(
                "Sepultamento não encontrado."
            )

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
        sepultamento = self.__auxiliar_busca_sepultamento(validar_cpf(cpf))

        if not sepultamento:
            raise ValueError("Esse sepultamento não existe")