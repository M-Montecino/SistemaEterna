from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional, Any

from models.exumacao import Exumacao
from models.sepultamento import Sepultamento
from models.tumulo import Tumulo, TipoTumulo
from views.tela_exumacao import TelaExumacao

if TYPE_CHECKING:
    from controllers.controlador_geral import ControladorGeral

class ControladorExumacao:
    def __init__(self, controlador_geral: "ControladorGeral"):
        self.__controlador_geral = controlador_geral
        self.__tela_exumacao = None

    def reinicia_tela(self):
        self.__tela_exumacao = None

#funções auxiliares
    def __validar_data(self, data: datetime):
        if not isinstance(data, datetime):
            raise ValueError("Data inválida.")
        
        data_atual = datetime.now().date()

        if data.date() < data_atual:
            raise ValueError(
                "A data da exumação não pode ser anterior à data atual."
            )

    def __validar_destino(self, destino: str):
        if not isinstance(destino, str) or destino.strip() == "":
            raise ValueError("Destino é obrigatório.")

    def __validar_dados_exumacao(self, dados: dict):
        self.__validar_data(dados["data"])
        self.__validar_destino(dados["destino"])

    def __concessao_vencida_ha_mais_de_30_dias(self, sepultamento: Sepultamento) -> bool:
        data_final = sepultamento.concessao.data_fim
        if data_final is None:
            return False
        return datetime.now() >= data_final + timedelta(days=30)

    def __sepultamento_ja_possui_exumacao(self, sepultamento: Sepultamento) -> bool:
        # busca no banco em vez da lista
        return Exumacao.buscar_por_cpf_falecido(sepultamento.falecido.cpf) is not None

    def __obter_sepultamentos_disponiveis(self) -> list:
        sepultamentos = Sepultamento.buscar_ativos()
        return [
            s for s in sepultamentos
            if self.__concessao_vencida_ha_mais_de_30_dias(s)
            and not self.__sepultamento_ja_possui_exumacao(s)
        ]
    
    def __cpf_falecido_sepultamento(self, sepultamento: Sepultamento) -> str:
        return str(sepultamento.falecido.cpf)
    
    def __normalizar(self, valor: Any) -> str:
        return str(valor).strip().lower()
    
    def __formatar_data(self, data: Any) -> str:
        if isinstance(data, datetime):
            return data.strftime("%d/%m/%Y")
        return str(data) if data is not None else ""

    def __formatar_tumulo(self, tumulo) -> str:
        if isinstance(tumulo, int):
            tumulo = Tumulo.buscar_por_codigo(tumulo)
        
        if tumulo is None:
            return "Túmulo não encontrado"
        
        return (
            f"Código {tumulo.codigo} | "
            f"Setor {tumulo.setor} | "
            f"Nº {tumulo.numero} | "
            f"{tumulo.tipo.name}"
        )

    def __formatar_sepultamento_para_tela(self, sepultamento: Sepultamento) -> dict:
        f = sepultamento.falecido
        texto = (
            f"Falecido: {f.nome} | CPF: {f.cpf} | "
            f"Falecimento: {self.__formatar_data(f.data_falecimento)} | "
            f"Sepultamento: {self.__formatar_data(sepultamento.data_sepultamento)} | "
            f"Túmulo: {self.__formatar_tumulo(sepultamento.tumulo)}"
        )
        return {
            "identificador": self.__cpf_falecido_sepultamento(sepultamento),
            "texto": texto,
            "objeto": sepultamento
        }

    def __formatar_exumacao_para_tela(self, exumacao: Exumacao) -> dict:
        sepultamento = Sepultamento.buscar_por_cpf(exumacao.sepultamento)
        
        if sepultamento:
            texto_sepultamento = self.__formatar_sepultamento_para_tela(
                sepultamento
            )["texto"]
        else:
            texto_sepultamento = f"CPF do falecido: {exumacao.sepultamento}"
        
        return {
            "codigo": exumacao.codigo,
            "data": self.__formatar_data(exumacao.data),
            "sepultamento": texto_sepultamento,
            "destino": exumacao.destino,
            "observacoes": exumacao.observacoes,
            "realizada": exumacao.realizada(),
            "objeto": exumacao
        }

    def __texto_busca_exumacao(self, exumacao: Exumacao) -> str:
        dados = self.__formatar_exumacao_para_tela(exumacao)
        return " ".join(
            self.__normalizar(v)
            for k, v in dados.items()
            if k != "objeto"
        )

    def __atualizar_lista_tela(self, exumacoes: list):
        self.__tela_exumacao.atualizar_lista_exumacoes(
            [self.__formatar_exumacao_para_tela(ex) for ex in exumacoes]
        )

#metodos principais
    def cadastrar_exumacao(self):
        try:
            disponiveis = self.__obter_sepultamentos_disponiveis()
            if not disponiveis:
                self.__tela_exumacao.mostra_mensagem(
                    "Não existem sepultamentos disponíveis para exumação."
                )
                return

            dados = self.__tela_exumacao.pega_dados_exumacao(
                [self.__formatar_sepultamento_para_tela(s) for s in disponiveis]
            )

            if dados is None:
                return

            self.__validar_dados_exumacao(dados)
            
            sepultamento = dados["sepultamento"]

            nova = Exumacao(
                codigo = None,   # banco gera
                data = dados["data"],
                sepultamento= sepultamento.falecido.cpf,
                destino = dados["destino"],
                observacoes = dados.get("observacoes", "")
            )

            nova.cadastrar()
            self.__tela_exumacao.mostra_mensagem(
                "Exumação cadastrada com sucesso."
            )
            self.filtrar_exumacoes()

        except ValueError as erro:
            self.__tela_exumacao.mostra_mensagem(
                f"Erro ao cadastrar exumação: {str(erro)}"
            )

    def alterar_exumacao(self):
        try:
            codigo  = self.__tela_exumacao.pega_codigo_exumacao_selecionada()
            exumacao = Exumacao.buscar_por_codigo(codigo)
            
            if not exumacao:
                raise ValueError("Exumação não encontrada.")
            
            somente_observacoes = exumacao.realizada()

            novos = self.__tela_exumacao.pega_novos_dados_exumacao(
                self.__formatar_exumacao_para_tela(exumacao),
                somente_observacoes
            )

            if novos is None:
                return
            
            if somente_observacoes:
                exumacao.observacoes = novos.get("observacoes", "")
                exumacao.alterar_observacoes()
            else:
                self.__validar_dados_exumacao(novos)

                exumacao.data = novos["data"]
                exumacao.destino = novos["destino"]
                exumacao.observacoes = novos.get("observacoes", "")

                exumacao.alterar()
            
            self.__tela_exumacao.mostra_mensagem(
                "Exumação atualizada com sucesso."
            )
            self.filtrar_exumacoes()

        except ValueError as erro:
            self.__tela_exumacao.mostra_mensagem(
                f"Erro ao alterar exumação: {str(erro)}"
            )

    def excluir_exumacao(self):
        try:
            codigo = self.__tela_exumacao.pega_codigo_exumacao_selecionada()
            exumacao = Exumacao.buscar_por_codigo(codigo)

            if not exumacao:
                raise ValueError("Exumação não encontrada.")
            
            if exumacao.realizada():
                raise ValueError(
                    "Exumação já realizada não pode ser excluída. "
                    "Apenas as observações podem ser alteradas."
                )

            if not self.__tela_exumacao.confirma_exclusao_exumacao(
                self.__formatar_exumacao_para_tela(exumacao)
            ):
                return

            exumacao.deletar()
            self.__tela_exumacao.mostra_mensagem(
                "Exumação excluída com sucesso."
            )
            self.filtrar_exumacoes()

        except ValueError as erro:
            self.__tela_exumacao.mostra_mensagem(
                f"Erro ao excluir exumação: {str(erro)}"
            )

    def filtrar_exumacoes(self):
        filtro    = self.__normalizar(self.__tela_exumacao.pega_dados_busca())
        exumacoes = Exumacao.buscar_todos()

        if filtro:
            exumacoes = [
                ex for ex in exumacoes
                if filtro in self.__texto_busca_exumacao(ex)
            ]

        self.__atualizar_lista_tela(exumacoes)

    def listar_exumacoes(self):
        self.__tela_exumacao.limpa_busca()
        self.filtrar_exumacoes()

    def retomar_menu(self):
        return

    def abre_tela(self):
        if self.__tela_exumacao is None:
            self.__tela_exumacao = TelaExumacao(self.__controlador_geral.tela_menu.root)

        listar_opcoes = {
            "cadastrar": self.cadastrar_exumacao,
            "filtrar": self.filtrar_exumacoes,
            "alterar": self.alterar_exumacao,
            "excluir": self.excluir_exumacao,
            "voltar": self.retomar_menu
        }

        self.filtrar_exumacoes()

        while True:
            try:
                opcao_escolhida = self.__tela_exumacao.tela_opcoes()
                funcao_escolhida = listar_opcoes.get(opcao_escolhida)

                if funcao_escolhida:
                    funcao_escolhida()

                    if opcao_escolhida == "voltar":
                        break
                else:
                    self.__tela_exumacao.mostra_mensagem(
                        "Opção inválida. Tente novamente."
                    )

            except ValueError as erro:
                self.__tela_exumacao.mostra_mensagem(
                    f"Erro: {str(erro)}"
                )
