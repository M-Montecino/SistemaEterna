from models.sepultamento import Sepultamento
from models.falecido import Falecido
from models.concessao import Concessao
from utils.funcoesAuxiliares import validar_cpf

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
        self.__tela_sepultamento = (TelaSepultamento(controlador_geral.tela_menu.root))

    def __buscar_sepultamento_por_cpf(
        self, cpf: str):
        for sep in (self.__sepultamentos):
            if (sep.falecido.cpf == cpf):
                return sep
        return None

    def __validar_data(self, data: datetime):
        if not isinstance(data, datetime):
            raise ValueError("Data inválida.")

    def __validar_valor(self, valor):
        if not isinstance(valor, (float)):
            raise ValueError("Valor inválido.")
        if valor < 0:
            raise ValueError("Valor negativo.")

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
            "Valor Pagamento:": concessao.valor_pagamento}

    def cadastrar_sepultamento(self):
        try:
            dados = (self.__tela_sepultamento.pega_dados_sepultamento())
            validar_cpf(dados['cpf_falecido'])

            if (self.__buscar_sepultamento_por_cpf(dados['cpf_falecido'])):
                self.__tela_sepultamento \
                    .mostra_mensagem("CPF já cadastrado.")
                return

            novo_sepultamento = (Sepultamento(
                    dados['cpf_falecido'],
                    dados['nome_falecido'],
                    dados['data_nascimento'],
                    dados['data_falecimento'],
                    dados['causa_morte'],

                    dados['tumulo'],

                    dados['valor_pagamento'],
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
            self.__tela_sepultamento.mostra_mensagem("Sepultamentocadastrado com sucesso.")
        except ValueError as erro:
            self.__tela_sepultamento.mostra_mensagem(f"Erro: {str(erro)}")

    def listar_sepultamentos(self):
        if not self.__sepultamentos:
            self.__tela_sepultamento.mostra_mensagem("Nenhum sepultamento cadastrado.")

            return

        for sepultamento in (self.__sepultamentos):
            self.__tela_sepultamento.mostra_mensagem(self.__formatar_sepultamento(sepultamento))

    def buscar_sepultamento(self):
        cpf = ( self.__tela_sepultamento.pega_cpf_busca())
        sepultamento = (self.__buscar_sepultamento_por_cpf(cpf))
        if sepultamento:
            self.__tela_sepultamento.mostra_mensagem(self.__formatar_sepultamento(sepultamento))
        else:
            self.__tela_sepultamento.mostra_mensagem("Sepultamento não encontrado.")

    def alterar_sepultamento(self):
        try:
            cpf = (self.__tela_sepultamento.pega_cpf_alteracao())
            sepultamento = (self.__buscar_sepultamento_por_cpf(cpf))
            if not sepultamento:
                self.__tela_sepultamento.mostra_mensagem("Sepultamento não encontrado.")
                return

            novas_observacoes = (self.__tela_sepultamento.pega_novas_observacoes())
            sepultamento.observacoes = (novas_observacoes)
            self.__tela_sepultamento.mostra_mensagem("Sepultamento alterado com sucesso.")
        except ValueError as erro:
            self.__tela_sepultamento.mostra_mensagem(f"Erro: {str(erro)}")

    def excluir_sepultamento(self):
        cpf = (self.__tela_sepultamento.pega_cpf_exclusao())
        sepultamento = (self.__buscar_sepultamento_por_cpf(cpf))
        if sepultamento:
            self.__sepultamentos.remove(sepultamento)
            self.__tela_sepultamento.mostra_mensagem("Sepultamento excluído com sucesso.")
        else:
            self.__tela_sepultamento.mostra_mensagem("Sepultamento não encontrado.")

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