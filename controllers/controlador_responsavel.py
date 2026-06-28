from models.responsavel import Responsavel
from views.tela_responsavel import TelaResponsavel
from utils.funcoesAuxiliares import validar_cep, validar_cpf, validar_email, validar_telefone
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controllers.controlador_geral import ControladorGeral

class ControladorResponsavel:
    def __init__(self, controlador_geral: "ControladorGeral"):
        self.__controlador_geral = (controlador_geral)
        self.__tela_responsavel = None

    def reinicia_tela(self):
        self.__tela_responsavel = None

#Funções auxiliares    
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
            'Email: ': responsavel.email,
            'Data de nascimento: ': responsavel.data_nascimento.strftime('%d/%m/%Y')
        }
    
#Funções principais
    def cadastrar_responsavel(self):
        try:
            dados = self.__tela_responsavel.pegar_dados_responsavel()
            if dados is None: return
            self.__validar_dados_responsavel(dados)

            if Responsavel.buscar_por_cpf(dados['cpf']):
                self.__tela_responsavel.mostra_mensagem(
                    "CPF já cadastrado."
                )
                return
            
            novo = Responsavel(
                dados['nome'],
                dados['cpf'],
                dados['telefone'],
                dados['cep'],
                dados['numero'],
                dados['email'],
                dados['data_nascimento']
            )

            novo.cadastrar()
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
            if cpf is None: return
            if not validar_cpf(cpf):
                raise ValueError("CPF inválido.")

            responsavel = Responsavel.buscar_por_cpf(cpf)
            if not responsavel:
                self.__tela_responsavel.mostra_mensagem(
                    "Responsável não encontrado."
                )
                return
            
            novos_dados = (
                self.__tela_responsavel.pega_novos_dados_responsavel()
            )
            if novos_dados is None: return

            dados_finais = {
                'cpf': cpf,
                'nome': novos_dados['nome'] if novos_dados['nome'] is not None else responsavel.nome,
                'telefone': novos_dados['telefone'] if novos_dados['telefone'] is not None else responsavel.telefone,
                'cep': novos_dados['cep'] if novos_dados['cep'] is not None else responsavel.cep,
                'numero': novos_dados['numero'] if novos_dados['numero'] is not None else responsavel.numero,
                'email': novos_dados['email'] if novos_dados['email'] is not None else responsavel.email,
                'data_nascimento': novos_dados['data_nascimento'] if novos_dados['data_nascimento'] is not None else responsavel.data_nascimento
            }

            self.__validar_dados_responsavel(dados_finais)

            #atualizando dados
            responsavel.nome = dados_finais['nome']   
            responsavel.telefone = dados_finais['telefone']
            responsavel.cep = dados_finais['cep']
            responsavel.numero = dados_finais['numero']
            responsavel.email = dados_finais['email']
            responsavel.data_nascimento = dados_finais['data_nascimento']

            responsavel.alterar()
            self.__tela_responsavel.mostra_mensagem(
                "Responsável atualizado com sucesso."
            )
        
        except ValueError as e:
            self.__tela_responsavel.mostra_mensagem(
                f"Erro ao alterar responsável: {str(e)}"
            )

    def excluir_responsavel(self):
        try:
            cpf = self.__tela_responsavel.excluir_responsavel()
            if cpf is None: return
            validar_cpf(cpf)

            responsavel = Responsavel.buscar_por_cpf(cpf)
            if not responsavel:
                self.__tela_responsavel.mostra_mensagem(
                    "Responsável não encontrado."
                )
                return
            
            responsavel.deletar()
            self.__tela_responsavel.mostra_mensagem(
                    "Responsável excluído com sucesso."
                )

        except ValueError as e:
            self.__tela_responsavel.mostra_mensagem(
                f"Erro ao alterar responsável: {str(e)}"
            )
    
    def listar_responsaveis(self):
        responsaveis = Responsavel.buscar_todos()

        if not responsaveis:
            self.__tela_responsavel.mostra_mensagem(
                "Nenhum responsável cadastrado."
            )
        
        for responsavel in responsaveis:
            self.__tela_responsavel.mostra_mensagem(
                self.__formatar_responsavel(responsavel)
            )

    def buscar_responsavel(self):
        try:
            cpf = self.__tela_responsavel.buscar_responsavel()
            if cpf is None: return
            validar_cpf(cpf)

            responsavel = Responsavel.buscar_por_cpf(cpf)            
            if responsavel:
                self.__tela_responsavel.mostra_mensagem(
                    self.__formatar_responsavel(responsavel)
                )
            else:
                self.__tela_responsavel.mostra_mensagem(
                    "Responsável não encontrado."
                )

        except ValueError as erro:
            self.__tela_responsavel.mostra_mensagem(
                f"Erro ao buscar responsável: {str(erro)}"
            )
        
    def retomar_menu(self):
        return
    
    def abre_tela(self):
        if self.__tela_responsavel is None:
            self.__tela_responsavel = TelaResponsavel(self.__controlador_geral.tela_menu.root)

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
        responsavel = Responsavel.buscar_por_cpf(cpf)

        if not responsavel:
            raise ValueError("Responsável não existe")