from models.responsavel import Responsavel
from views.tela_responsavel import TelaResponsavel
from utils.funcoesAuxiliares import validar_cep, validar_cpf, validar_email, validar_telefone
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controllers.controlador_geral import ControladorGeral

class ControladorResponsavel:
    def __init__(
        self, 
        controlador_geral: "ControladorGeral"):
        self.__responsaveis = []
        self.__controlador_geral = (controlador_geral)
        self.__tela_responsavel = TelaResponsavel(controlador_geral.tela_menu.root)

#Funções auxiliares
    def __auxiliar_busca_responsavel(self, cpf: int):
        for responsavel in self.__responsaveis:
            if responsavel.cpf == cpf:
                return responsavel
        return None
    
    def __validar_nome(self, nome):
        if not isinstance(nome, str):
            raise ValueError("Nome precisa ser uma string")
        
        if len(nome.strip()) == 0:
            raise ValueError("O nome não pode estar vazio")
        
    def __validar_numero(self, numero):
        if not isinstance(numero, int):
            raise ValueError("Numero precisa ser inteiro")
        
        if numero < 0:
            raise ValueError("Numero precisa ser positivo")
    
    def __validar_dados_responsavel(self, dados):
        self.__validar_nome(dados['nome'])
        if not validar_cpf(dados['cpf']):
            raise ValueError("CPF inválido")
        if not validar_telefone(dados['telefone']):
            raise ValueError("Telefone inválido")
        if not validar_cep(dados['cep']):
            raise ValueError("CEP inválido")
        self.__validar_numero(dados['numero'])
        if not validar_email(dados['email']):
            raise ValueError("Email inválido")
    
    def __formatar_responsavel(self, responsavel):
        return {
            'Nome: ': responsavel.nome,
            'Cpf:': responsavel.cpf,
            'Telefone: ': responsavel.telefone,
            'Cep: ': responsavel.cep,
            'Numero: ': responsavel.numero,
            'Email: ': responsavel.email
        }
    
#Funções principais
    def cadastrar_responsavel(self):
        try:
            dados_responsavel = self.__tela_responsavel.pegar_dados_responsavel()
            self.__validar_dados_responsavel(dados_responsavel)

            if self.__auxiliar_busca_responsavel(dados_responsavel['cpf']) is not None:
                self.__tela_responsavel.mostra_mensagem(
                    "CPF já cadastrado."
                )
                return
            
            novo_responsavel = Responsavel(
                dados_responsavel['nome'],
                dados_responsavel['cpf'],
                dados_responsavel['telefone'],
                dados_responsavel['cep'],
                dados_responsavel['numero'],
                dados_responsavel['email']
            )

            self.__responsavels.append(novo_responsavel)
            self.__tela_responsavel.mostra_mensagem(
                "Responsável cadastrado com sucesso."
            )

        except ValueError as e:
            self.__tela_responsavel.mostra_mensagem(
                f"Erro ao cadastrar responsável: {str(e)}"
            )

    def alterar_responsavel(self):
        try:
            cpf = self.__tela_responsavel.alterar_responsavel()
            validar_cpf(cpf)
            responsavel = self.__auxiliar_busca_responsavel(cpf)
            responsavel_atualizado = responsavel

            if not responsavel:
                self.__tela_responsavel.mostra_mensagem(
                    "Responsável não encontrado."
                )
                return
            
            novos_dados = (
                self.__tela_responsavel.pega_dados_responsavel()
            )

            #atualizando dados
            if novos_dados['nome'] is not None:
                responsavel_atualizado.nome = novos_dados['nome']   
            if novos_dados['telefone'] is not None:
                responsavel_atualizado.telefone = novos_dados['telefone']
            if novos_dados['cep'] is not None:
                responsavel_atualizado.cep = novos_dados['cep']
            if novos_dados['numero'] is not None:
                responsavel_atualizado.numero = novos_dados['numero']
            if novos_dados['email'] is not None:
                responsavel_atualizado.email = novos_dados['email']

            self.__validar_dados_responsavel(responsavel_atualizado)
            responsavel = responsavel_atualizado

            self.__tela_responsavel.mostra_mensagem(
                "Responsável atualizado com sucesso."
            )
        
        except ValueError as e:
            self.__tela_responsavel.mostra_mensagem(
                f"Erro ao alterar responsável: {str(e)}"
            )

    def excluir_responsavel(self):
        cpf = self.__tela_responsavel.excluir_responsavel()
        validar_cpf(cpf)
        responsavel = self.__auxiliar_busca_responsavel(cpf)

        if responsavel:
            self.__responsaveis.remove(responsavel)
            self.__tela_responsavel.mostra_mensagem(
                "Responsável excluído com sucesso."
            )
        else:
            self.__tela_responsavel.mostra_mensagem(
                "Responsável não encontrado."
            )
    
    def listar_responsaveis(self):
        if not self.__responsaveis:
            self.__tela_responsavel.mostra_mensagem(
                "Nenhum responsável cadastrado."
            )
        
        for responsavel in self.__responsaveis:
            self.__tela_responsavel.mostra_mensagem(
                self.__formatar_responsavel(responsavel)
            )

    def buscar_responsavel(self):
        cpf = self.__tela_responsavel.buscar_responsavel()
        validar_cpf(cpf)
        responsavel = self.__auxiliar_busca_responsavel(cpf)
        
        if responsavel:
            self.__tela_responsavel.mostra_mensagem(
                self.__formatar_responsavel(responsavel)
            )
        else:
            self.__tela_responsavel.mostra_mensagem(
                "Responsável não encontrado."
            )
        
    def retomar_menu(self):
        return
    
    def abre_tela(self):
        listar_opcoes = {
            1: self.cadastrar_responsavel,
            2: self.alterar_responsavel,
            3: self.excluir_responsavel,
            4: self.listar_responsaveis,
            5: self.buscar_responsavel,
            0: self.retomar_menu
        }
    
        while True:
            try:
                opcao_escolhida = self.__tela_responsavel.tela_opcoes()
                funcao_escolhida = listar_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    funcao_escolhida()
                    if opcao_escolhida == 0:
                        break
                else:
                    self.__tela_responsavel.mostra_mensagem(
                        "Opção inválida. Tente novamente.")
            except ValueError as e:
                self.__tela_responsavel.mostra_mensagem(
                    f"Erro: {str(e)}")
                
    def validar_responsavel(self, cpf):
        responsavel = self.__auxiliar_busca_responsavel(validar_cpf(cpf))

        if not responsavel:
            raise ValueError("Responsável não existe")