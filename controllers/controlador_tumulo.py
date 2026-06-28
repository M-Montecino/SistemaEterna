from models.tumulo import Tumulo, TipoTumulo
from views.tela_tumulo import TelaTumulo
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controllers.controlador_geral import ControladorGeral

class ControladorTumulo:
    def __init__(
        self,
        controlador_geral: "ControladorGeral"):
        self.__controlador_geral = (controlador_geral)
        self.__tela_tumulo = None

    def reinicia_tela(self):
        self.__tela_tumulo = None

#Funções auxiliares
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
        
    def __formatar_tumulo(self, tumulo):
        return (
            f"Código: {tumulo.codigo}\n"
            f"Setor: {tumulo.setor}\n"
            f"Número: {tumulo.numero}\n"
            f"Tipo: {tumulo.tipo.name if hasattr(tumulo.tipo, 'name') else tumulo.tipo}\n"
            f"Capacidade: {tumulo.capacidade}"
        )
    
#Funções principais
    def cadastrar_tumulo(self):
        try:
            dados = self.__tela_tumulo.pega_dados_tumulo()
            if dados is None: return
            self.__validar_dados_tumulo(dados)

            if Tumulo.buscar_por_codigo(dados['codigo']):
                self.__tela_tumulo.mostra_mensagem(
                    "Código de túmulo já cadastrado."
                )
                return

            tipo = TipoTumulo(int(dados['tipo']))



            novo = Tumulo(
                dados['codigo'],
                dados['setor'], 
                dados['numero'], 
                tipo,
                dados['capacidade']
            )


            novo.cadastrar()
            self.__tela_tumulo.mostra_mensagem(
                "Túmulo cadastrado com sucesso."
            )

        except ValueError as erro:
            self.__tela_tumulo.mostra_mensagem(
                f"Erro ao cadastrar túmulo: {str(erro)}"
            )

    def alterar_tumulo(self):
        try:
            codigo = self.__tela_tumulo.alterar_tumulo()
            if codigo is None: return
            codigo = int(codigo)
            self.__validar_numeros(codigo)

            tumulo = Tumulo.buscar_por_codigo(codigo)
            if not tumulo:
                self.__tela_tumulo.mostra_mensagem(
                    "Túmulo não encontrado."
                    )
                return
            
            novos_dados = (
                self.__tela_tumulo.pega_novos_dados_tumulo()
            )
            if novos_dados is None: return


            dados_finais = {
                'codigo': codigo,
                'setor': novos_dados['setor'] if novos_dados['setor'] is not None else tumulo.setor,
                'numero': novos_dados['numero'] if novos_dados['numero'] is not None else tumulo.numero,
                'tipo': novos_dados['tipo'] if novos_dados['tipo'] is not None else tumulo.tipo,
                'capacidade': novos_dados['capacidade'] if novos_dados['capacidade'] is not None else tumulo.capacidade
            }

            self.__validar_dados_tumulo(dados_finais)
            tipo_tumulo = self.__converter_tipo_tumulo(dados_finais['tipo'])

            #atualizando dados
            tumulo.setor = dados_finais['setor']
            tumulo.numero = dados_finais['numero']
            tumulo.tipo = tipo_tumulo
            print(type(tipo_tumulo))
            print(tipo_tumulo)
            tumulo.capacidade = dados_finais['capacidade']

            tumulo.alterar()
            self.__tela_tumulo.mostra_mensagem(
                "Túmulo alterado com sucesso."
            )

        except ValueError as erro:
            self.__tela_tumulo.mostra_mensagem(
                f"Erro ao alterar túmulo: {str(erro)}"
            )

    def excluir_tumulo(self):
        try:
            codigo = self.__tela_tumulo.excluir_tumulo()
            if codigo is None: return
            codigo = int(codigo)
            self.__validar_numeros(codigo)

            tumulo = Tumulo.buscar_por_codigo(codigo)
            if not tumulo:
                self.__tela_tumulo.mostra_mensagem("Túmulo não encontrado")
                return
            
            tumulo.deletar()
            self.__tela_tumulo.mostra_mensagem("Túmulo excluído com sucesso.")

        except ValueError as erro:
            self.__tela_tumulo.mostra_mensagem(
                f"Erro ao excluir túmulo: {str(erro)}"
            )
        
    def listar_tumulos(self):
        tumulos = Tumulo.buscar_todos()

        if not tumulos:
            self.__tela_tumulo.mostra_mensagem("Nenhum túmulo cadastrado.")
            return

        texto = "\n\n".join(self.__formatar_tumulo(t) for t in tumulos)
        self.__tela_tumulo.mostra_mensagem(texto)

    def buscar_tumulo(self):
        try:
            codigo = self.__tela_tumulo.excluir_tumulo()
            if codigo is None: return
            codigo = int(codigo)
            self.__validar_numeros(codigo)

            tumulo = Tumulo.buscar_por_codigo(codigo)
            if tumulo:
                self.__tela_tumulo.mostra_mensagem(
                    self.__formatar_tumulo(tumulo)
                )
            else:
                self.__tela_tumulo.mostra_mensagem(
                "Túmulo não encontrado"
                )
        except ValueError as erro:
            self.__tela_tumulo.mostra_mensagem(
                f"Erro ao buscar túmulo: {str(erro)}"
            )
            
    def gerar_relatorio_ocupacao(self):
        relatorio = Tumulo.buscar_dados_ocupacao()

        if not relatorio:
            self.__tela_tumulo.mostra_mensagem(
                "Nenhum túmulo cadastrado para gerar relatório."
            )
            return

        self.__tela_tumulo.mostra_relatorio_ocupacao(relatorio)

    def retomar_menu(self):
        return
    
    def abre_tela(self):
        if self.__tela_tumulo is None:
            self.__tela_tumulo = TelaTumulo(self.__controlador_geral.tela_menu.root)

        listar_opcoes = {
            1: self.cadastrar_tumulo,
            2: self.alterar_tumulo,
            3: self.excluir_tumulo,
            4: self.listar_tumulos,
            5: self.buscar_tumulo,
            6: self.gerar_relatorio_ocupacao,
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
        tumulo = Tumulo.buscar_por_codigo(codigo)

        if not tumulo:
            raise ValueError("Esse túmulo não existe")
        
        if tumulo.esta_lotado():
            raise ValueError("Túmulo atingiu a capacidade máxima. Não é possível realizar novos sepultamentos.")