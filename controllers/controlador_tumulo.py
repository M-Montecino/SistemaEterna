from models.tumulo import Tumulo, TipoTumulo
from views.tela_tumulo import TelaTumulo
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controllers.controlador_geral import ControladorGeral

class ControladorTumulo:
    def __init__(
        self,
        controlador_geral: "ControladorGeral"):
        self.__tumulos = []
        self.__controlador_geral = (controlador_geral)
        self.__tela_tumulo = TelaTumulo(controlador_geral.tela_menu.root)

#Funções auxiliares
    def __auxiliar_busca_tumulo(self, codigo: int):
        for tumulo in self.__tumulos:
            if tumulo.codigo == codigo:
                return tumulo
        return None

    def __validar_numeros(self, numero):
        if not isinstance(numero, int):
            raise ValueError("O número deve ser um inteiro.")
        
        if numero <= 0:
            raise ValueError("O número deve ser positivo.")
    
        if numero > 999999:
            raise ValueError("Número muito grande.")
        
    def __validar_setor(self, setor):
        if not isinstance(setor, str):
            raise ValueError("O setor deve ser uma string.")
        
        if len(setor.strip()) == 0:
            raise ValueError("O setor não pode ser vazio.")
        
    def __converter_tipo_tumulo(self, tipo):
        if isinstance(tipo, TipoTumulo):
            return tipo

        if isinstance(tipo, str):
            texto = tipo.strip()
            if texto.isdigit():
                try:
                    return TipoTumulo(int(texto))
                except ValueError:
                    pass

            texto_normalizado = texto.strip().upper()
            try:
                return TipoTumulo[texto_normalizado]
            except KeyError:
                raise ValueError("Tipo de túmulo inválido.")

        if isinstance(tipo, int):
            try:
                return TipoTumulo(tipo)
            except ValueError:
                pass

        raise ValueError("Tipo de túmulo inválido.")
    
    def __validar_dados_tumulo(self, dados):
        self.__validar_numeros(dados['codigo'])
        self.__validar_setor(dados['setor'])
        self.__validar_numeros(dados['numero'])
        tipo_tumulo = self.__converter_tipo_tumulo(dados['tipo'])
        self.__validar_numeros(dados['capacidade'])

        if tipo_tumulo == TipoTumulo.Cova and dados['capacidade'] != 1:
            raise ValueError("Capacidade inválida para túmulo do tipo Cova. Deve ser 1.")
        
        if dados['numero'] < dados['capacidade']:
            raise ValueError("Número do túmulo não pode ser menor que a capacidade.")
        
    def __formatar_tumulo(self, tumulo):
        return {
            "Código: ": tumulo.codigo,
            "Setor: ": tumulo.setor,
            "Número: ": tumulo.numero,
            "Tipo: ": tumulo.tipo,
            "Capacidade ": tumulo.capacidade
        }
    
#Funções principais
    def cadastrar_tumulo(self):
        try:
            dados_tumulo = self.__tela_tumulo.pega_dados_tumulo()
            self.__validar_dados_tumulo(dados_tumulo)

            if self.__auxiliar_busca_tumulo(dados_tumulo['codigo']) is not None:
                self.__tela_tumulo.mostra_mensagem(
                    "Código de túmulo já cadastrado."
                )
                return

            novo_tumulo = Tumulo(
                dados_tumulo['codigo'],
                dados_tumulo['setor'], 
                dados_tumulo['numero'], 
                dados_tumulo['tipo'], 
                dados_tumulo['capacidade']
            )


            self.__tumulos.append(novo_tumulo)
            self.__tela_tumulo.mostra_mensagem(
                "Túmulo cadastrado com sucesso."
            )

        except ValueError as e:
            self.__tela_tumulo.mostra_mensagem(
                f"Erro ao cadastrar túmulo: {str(e)}"
            )

    def alterar_tumulo(self):
        try:
            codigo = self.__tela_tumulo.alterar_tumulo()
            self.__validar_numeros(codigo)
            tumulo = self.__auxiliar_busca_tumulo(codigo)
            tumulo_atualizado = tumulo

            if not tumulo:
                self.__tela_tumulo.mostra_mensagem(
                    "Túmulo não encontrado."
                )
                return
            
            novos_dados = (
                self.__tela_tumulo.pega_dados_tumulo()
            )

            #atualizando dados
            if novos_dados['setor'] is not None:
                tumulo_atualizado.setor = novos_dados['setor']
            if novos_dados['numero'] is not None:
                tumulo_atualizado.numero = novos_dados['numero']
            if novos_dados['tipo'] is not None:
                tumulo_atualizado.tipo = novos_dados['tipo']
            if novos_dados['capacidade'] is not None:
                tumulo_atualizado.capacidade = novos_dados['capacidade']

            self.__validar_dados_tumulo(tumulo_atualizado)
            tumulo = tumulo_atualizado

            self.__tela_tumulo.mostra_mensagem(
                "Túmulo alterado com sucesso."
            )

        except ValueError as erro:
            self.__tela_tumulo.mostra_mensagem(
                f"Erro ao alterar túmulo: {str(erro)}"
            )

    def excluir_tumulo(self):
        codigo = self.__tela_tumulo.excluir_tumulo()
        tumulo = self.__auxiliar_busca_tumulo(codigo)

        if tumulo:
            self.__tumulos.remove(tumulo)
            self.__tela_tumulo.mostra_mensagem(
                "Túmulo excluido com sucesso"
            )
        else:
            self.__tela_tumulo.mostra_mensagem(
                "Túmulo não encontrado"
            )
        
    def listar_tumulos(self):
        if not self.__tumulos:
            self.__tela_tumulo.mostra_mensagem("" \
            "Nenhum túmulo cadastrado")
            return
        
        for tumulo in self.__tumulos:
            self.__tela_tumulo.mostra_mensagem(
                self.__formatar_tumulo(tumulo)
            )

    def buscar_tumulo(self):
        codigo = self.__tela_tumulo.buscar_tumulo()
        tumulo = self.__auxiliar_busca_tumulo(codigo)
        if tumulo:
            self.__tela_tumulo.mostra_mensagem(
                self.__formatar_tumulo(tumulo)
            )
        else:
            self.__tela_tumulo.mostra_mensagem("" \
            "Túmulo não encontrado")

    def retomar_menu(self):
        return
    
    def abre_tela(self):
        listar_opcoes = {
            1: self.cadastrar_tumulo,
            2: self.alterar_tumulo,
            3: self.excluir_tumulo,
            4: self.listar_tumulos,
            5: self.buscar_tumulo,
            0: self.retomar_menu
        }
    
        while True:
            try:
                opcao_escolhida = self.__tela_tumulo.tela_opcoes()
                funcao_escolhida = listar_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    funcao_escolhida()
                    if opcao_escolhida == 0:
                        break
                else:
                    self.__tela_tumulo.mostra_mensagem(
                        "Opção inválida. Tente novamente.")
            except ValueError as e:
                self.__tela_tumulo.mostra_mensagem(
                    f"Erro: {str(e)}")
                
    def validar_tumulo(self, codigo):
        tumulo = self.__auxiliar_busca_tumulo(codigo)

        if not tumulo:
            raise ValueError("Esse túmulo não existe")