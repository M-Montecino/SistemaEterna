from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional, Any

from models.exumacao import Exumacao
from models.sepultamento import Sepultamento
from views.tela_exumacao import TelaExumacao

if TYPE_CHECKING:
    from controllers.controlador_geral import ControladorGeral

class ControladorExumacao:
    def __init__(self, controlador_geral: "ControladorGeral"):
        self.__exumacoes: list[Exumacao] = []
        self.__controlador_geral = controlador_geral
        self.__tela_exumacao = TelaExumacao(controlador_geral.tela_menu.root)

    @property
    def exumacoes(self):
        return self.__exumacoes

    def __auxiliar_busca_exumacao(self, codigo: int) -> Optional[Exumacao]:
        for exumacao in self.__exumacoes:
            if exumacao.codigo == codigo:
                return exumacao
        return None

    def __cpf_falecido_sepultamento(self, sepultamento: Sepultamento) -> str:
        if sepultamento is None:
            return ""

        falecido = getattr(sepultamento, "falecido", None)
        cpf = getattr(falecido, "cpf", None)

        if cpf is None:
            return str(id(sepultamento))

        return str(cpf)

    def __auxiliar_busca_exumacao_por_sepultamento(
        self,
        sepultamento: Sepultamento
    ) -> Optional[Exumacao]:
        cpf_sepultamento = self.__cpf_falecido_sepultamento(sepultamento)

        for exumacao in self.__exumacoes:
            cpf_exumacao = self.__cpf_falecido_sepultamento(
                exumacao.sepultamento
            )
            if cpf_exumacao == cpf_sepultamento:
                return exumacao

        return None

    def __validar_codigo(self, codigo: int):
        if not isinstance(codigo, int):
            raise ValueError("O código deve ser um inteiro.")

        if codigo <= 0:
            raise ValueError("O código deve ser positivo.")

    def __validar_data(self, data: datetime):
        if not isinstance(data, datetime):
            raise ValueError("Data inválida.")

    def __validar_destino(self, destino: str):
        if not isinstance(destino, str) or destino.strip() == "":
            raise ValueError("Destino é obrigatório.")

    def __validar_dados_exumacao(self, dados: dict):
        self.__validar_data(dados["data"])
        self.__validar_destino(dados["destino"])

    def __gerar_codigo_exumacao(self) -> int:
        maior_codigo = 0

        for exumacao in self.__exumacoes:
            codigo = getattr(exumacao, "codigo", 0)

            if isinstance(codigo, int) and codigo > maior_codigo:
                maior_codigo = codigo

        novo_codigo = maior_codigo + 1

        while self.__auxiliar_busca_exumacao(novo_codigo) is not None:
            novo_codigo += 1

        return novo_codigo

    def __obter_sepultamentos(self) -> list[Sepultamento]:
        controlador_sepultamento = (
            self.__controlador_geral.controlador_sepultamento
        )

        if controlador_sepultamento is None:
            raise ValueError(
                "Controlador de sepultamento não foi inicializado."
            )

        return list(controlador_sepultamento.sepultamentos)

    def __obter_data_final_concessao(
        self,
        sepultamento: Sepultamento
    ) -> Optional[datetime]:
        concessao = getattr(sepultamento, "concessao", None)

        if concessao is None:
            return None

        data_final = getattr(concessao, "data_final_cons", None)

        if not isinstance(data_final, datetime):
            return None

        return data_final

    def __concessao_vencida_ha_mais_de_30_dias(
        self,
        sepultamento: Sepultamento
    ) -> bool:
        data_final = self.__obter_data_final_concessao(sepultamento)

        if data_final is None:
            return False

        data_minima_para_exumacao = data_final + timedelta(days=30)

        return datetime.now() >= data_minima_para_exumacao

    def __sepultamento_ja_possui_exumacao(
        self,
        sepultamento: Sepultamento
    ) -> bool:
        return (
            self.__auxiliar_busca_exumacao_por_sepultamento(sepultamento)
            is not None
        )

    # concessão do sepultamento deve estar vencida há mais de 30 dias;
    # sepultamento ainda não pode estar associado a uma exumação.
    def __obter_sepultamentos_disponiveis(self) -> list[Sepultamento]:
        sepultamentos = self.__obter_sepultamentos()
        sepultamentos_disponiveis = []

        for sepultamento in sepultamentos:
            if not self.__concessao_vencida_ha_mais_de_30_dias(sepultamento):
                continue

            if self.__sepultamento_ja_possui_exumacao(sepultamento):
                continue

            sepultamentos_disponiveis.append(sepultamento)

        return sepultamentos_disponiveis

    def __formatar_data(self, data: Any) -> str:
        if isinstance(data, datetime):
            return data.strftime("%d/%m/%Y")
        return str(data) if data is not None else ""

    def __formatar_tumulo(self, tumulo: Any) -> str:
        if tumulo is None:
            return ""

        codigo = getattr(tumulo, "codigo", None)
        setor = getattr(tumulo, "setor", None)
        numero = getattr(tumulo, "numero", None)
        tipo = getattr(tumulo, "tipo", None)

        partes = []

        if codigo is not None:
            partes.append(f"Código {codigo}")
        if setor is not None:
            partes.append(f"Setor {setor}")
        if numero is not None:
            partes.append(f"Nº {numero}")
        if tipo is not None:
            nome_tipo = getattr(tipo, "name", str(tipo))
            partes.append(str(nome_tipo))

        if partes:
            return " | ".join(partes)

        return str(tumulo)

    def __formatar_sepultamento_para_tela(
        self,
        sepultamento: Sepultamento
    ) -> dict:
        falecido = sepultamento.falecido

        nome = getattr(falecido, "nome", "")
        cpf = getattr(falecido, "cpf", "")
        data_falecimento = self.__formatar_data(
            getattr(falecido, "data_falecimento", None)
        )
        data_sepultamento = self.__formatar_data(
            getattr(sepultamento, "data_sepultamento", None)
        )
        tumulo = self.__formatar_tumulo(getattr(sepultamento, "tumulo", None))

        texto = (
            f"Falecido: {nome} | CPF: {cpf} | "
            f"Falecimento: {data_falecimento} | "
            f"Sepultamento: {data_sepultamento} | Túmulo: {tumulo}"
        )

        return {
            "identificador": self.__cpf_falecido_sepultamento(sepultamento),
            "texto": texto,
            "objeto": sepultamento
        }

    def __formatar_exumacao_para_tela(self, exumacao: Exumacao) -> dict:
        return {
            "codigo": exumacao.codigo,
            "data": self.__formatar_data(exumacao.data),
            "sepultamento": self.__formatar_sepultamento_para_tela(
                exumacao.sepultamento
            )["texto"],
            "destino": exumacao.destino,
            "observacoes": exumacao.observacoes,
            "objeto": exumacao
        }

    def __normalizar(self, valor: Any) -> str:
        return str(valor).strip().lower()

    def __texto_busca_exumacao(self, exumacao: Exumacao) -> str:
        dados = self.__formatar_exumacao_para_tela(exumacao)
        return " ".join(
            self.__normalizar(valor)
            for chave, valor in dados.items()
            if chave != "objeto"
        )

    def __atualizar_lista_tela(self, exumacoes: list[Exumacao]):
        self.__tela_exumacao.atualizar_lista_exumacoes(
            [self.__formatar_exumacao_para_tela(ex) for ex in exumacoes]
        )

    def cadastrar_exumacao(self):
        try:
            sepultamentos_disponiveis = self.__obter_sepultamentos_disponiveis()

            if not sepultamentos_disponiveis:
                self.__tela_exumacao.mostra_mensagem(
                    "Não existem sepultamentos disponíveis para exumação."
                )
                return

            dados_exumacao = self.__tela_exumacao.pega_dados_exumacao(
                [
                    self.__formatar_sepultamento_para_tela(sepultamento)
                    for sepultamento in sepultamentos_disponiveis
                ]
            )

            if dados_exumacao is None:
                return

            self.__validar_dados_exumacao(dados_exumacao)
            codigo = self.__gerar_codigo_exumacao()

            nova_exumacao = Exumacao(
                codigo,
                dados_exumacao["data"],
                dados_exumacao["sepultamento"],
                dados_exumacao["destino"],
                dados_exumacao.get("observacoes", "")
            )

            self.__exumacoes.append(nova_exumacao)
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
            codigo = self.__tela_exumacao.pega_codigo_exumacao_selecionada()
            self.__validar_codigo(codigo)

            exumacao = self.__auxiliar_busca_exumacao(codigo)

            if exumacao is None:
                self.__tela_exumacao.mostra_mensagem(
                    "Exumação não encontrada."
                )
                return

            novos_dados = self.__tela_exumacao.pega_novos_dados_exumacao(
                self.__formatar_exumacao_para_tela(exumacao)
            )

            if novos_dados is None:
                return

            dados_para_validar = {
                "data": novos_dados["data"],
                "destino": novos_dados["destino"],
                "observacoes": novos_dados.get("observacoes", "")
            }

            self.__validar_dados_exumacao(dados_para_validar)

            exumacao.data = novos_dados["data"]
            exumacao.destino = novos_dados["destino"]
            exumacao.observacoes = novos_dados.get("observacoes", "")

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
            self.__validar_codigo(codigo)

            exumacao = self.__auxiliar_busca_exumacao(codigo)

            if exumacao is None:
                self.__tela_exumacao.mostra_mensagem(
                    "Exumação não encontrada."
                )
                return

            confirmou = self.__tela_exumacao.confirma_exclusao_exumacao(
                self.__formatar_exumacao_para_tela(exumacao)
            )

            if not confirmou:
                return

            self.__exumacoes.remove(exumacao)
            self.__tela_exumacao.mostra_mensagem(
                "Exumação excluída com sucesso."
            )
            self.filtrar_exumacoes()

        except ValueError as erro:
            self.__tela_exumacao.mostra_mensagem(
                f"Erro ao excluir exumação: {str(erro)}"
            )

    def filtrar_exumacoes(self):
        filtro = self.__tela_exumacao.pega_dados_busca()
        filtro = self.__normalizar(filtro)

        if filtro == "":
            exumacoes_filtradas = self.__exumacoes
        else:
            exumacoes_filtradas = [
                exumacao
                for exumacao in self.__exumacoes
                if filtro in self.__texto_busca_exumacao(exumacao)
            ]

        self.__atualizar_lista_tela(exumacoes_filtradas)

    def listar_exumacoes(self):
        self.__tela_exumacao.limpa_busca()
        self.filtrar_exumacoes()

    def retomar_menu(self):
        return

    def abre_tela(self):
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
