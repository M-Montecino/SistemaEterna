from models.manutencao import Manutencao
from controllers.controlador_geral import ControladorGeral
from views.tela_manutencao import TelaManutencao

class ControladorManutencao:
    def __init__(self, controlador_geral: "ControladorGeral"):
        self.__manutencoes = []
        self.__controlador_geral = controlador_geral
        self.__tela_manutencao = TelaManutencao()

    def auxiliar_busca_manutencao(self, codigo: int):
        for manutencao in self.__manutencoes:
            if manutencao.codigo == codigo:
                return manutencao
            return None

    def cadastrar_manutencao(self):
        dados_manutencao = self.__tela_manutencao.pega_dados_manutencao()
        nova_manutencao = Manutencao(
            dados_manutencao['codigo'],
            dados_manutencao['tumulo'],
            dados_manutencao['tipo_servico'],
            dados_manutencao['data'],
            dados_manutencao['cpf_responsavel'] 
        )

        for manutencao in self.__manutencoes:
            if manutencao.codigo == nova_manutencao.codigo:
                self.__tela_manutencao.mostra_mensagem(
                    "Código de manutenção já existe"
                )
                return
            
        self.__manutencoes.append(nova_manutencao)
        self.__tela_manutencao.mostra_mensagem(
            "Manutenção adicionada com sucesso"
        )
        return
        
    def alterar_manutencao(self):
        codigo = self.__tela_manutencao.alterar_manutencao()
        manutencao = self.auxiliar_busca_manutencao(codigo)
        if manutencao:
            novos_dados = self.__tela_manutencao.pega_novos_dados_manutencao()

            manutencao.tumulo = novos_dados['tumulo']
            manutencao.tipo_servico = novos_dados['tipo_servico']
            manutencao.data = novos_dados['data']
            manutencao.cpf_responsavel = novos_dados['cpf_responsavel']
            self.__tela_manutencao.mostra_mensagem("" \
            "Manutenção alterada com sucesso")

        else:
            self.__tela_manutencao.mostra_mensagem(
                "Manutenção não encontrada"
            )
    
    def excluir_manutencao(self):
        codigo = self.__tela_manutencao.excluir_manutencao()
        manutencao = self.auxiliar_busca_manutencao(codigo)

        if manutencao:
            self.__manutencoes.remove(manutencao)
            self.__tela_manutencao.mostra_mensagem(
                "Manutenção excluída com sucesso"
            )
        else:
            self.__tela_manutencao.mostra_mensagem(
                "Manutenção não encontrada"
            )

    def listar_manutencoes(self):
        if not self.__manutencoes:
            self.__tela_manutencao.mostra_mensagem("" \
            "Nenhuma manutenção cadastrada")
            return
        
        for manutencao in self.__manutencoes:
            self.__tela_manutencao.mostra_mensagem({
                "Código:": manutencao.codigo,
                "Túmulo:": manutencao.tumulo,
                "Tipo de Serviço:": manutencao.tipo_servico.name,
                "Data:": manutencao.data.strftime("%d/%m/%Y"),
                "CPF do Responsável:": manutencao.cpf_responsavel
            })

    def buscar_manutencao(self):
        codigo = self.__tela_manutencao.buscar_manutencao()
        manutencao = self.auxiliar_busca_manutencao(codigo)
        if manutencao:
            self.__tela_manutencao.mostra_mensagem({
                "Código:": manutencao.codigo,
                "Túmulo:": manutencao.tumulo,
                "Tipo de Serviço:": manutencao.tipo_servico.name,
                "Data:": manutencao.data.strftime("%d/%m/%Y"),
                "CPF do Responsável:": manutencao.cpf_responsavel
            })
        else:
            self.__tela_manutencao.mostra_mensagem(
                "Manutenção não encontrada"
            )

    def retomar_menu(self):
        self.__controlador_geral.abre_tela()

    def abre_tela(self):
        listar_opcoes = {
            1: self.cadastrar_manutencao,
            2: self.alterar_manutencao,
            3: self.excluir_manutencao,
            4: self.listar_manutencoes,
            5: self.buscar_manutencao,
            0: self.retomar_menu
        }

        while True:
            try:
                opcao_escolhida = self.__tela_manutencao.tela_opcoes()
                funcao_escolhida = listar_opcoes.get(opcao_escolhida)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    self.__tela_manutencao.mostra_mensagem(
                        "Opção inválida. Tente novamente.")
            except Exception as e:
                self.__tela_manutencao.mostra_mensagem(
                    f"Comando inesperado: {str(e)}")