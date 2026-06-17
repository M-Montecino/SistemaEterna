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
        self.__exumacoes = []
        self.__sepultamentos_teste = self.__criar_sepultamentos_teste()
        self.__controlador_geral = controlador_geral
        self.__tela_exumacao = TelaExumacao(controlador_geral.tela_menu.root)

    @property
    def exumacoes(self):
        return self.__exumacoes
    
    def __criar_sepultamentos_teste(self) -> list[Sepultamento]:
        # Esta lista substitui temporariamente a busca no ControladorSepultamento,
        # permitindo testar sepultamentos elegiveis e nao elegiveis para exumacao.
        hoje = datetime.now()

        def criar_sepultamento(
            cpf_falecido: str,
            nome_falecido: str,
            codigo_tumulo: int,
            setor: str,
            numero_tumulo: int,
            data_final_cons: datetime,
            observacoes: str
        ) -> Sepultamento:
            data_nascimento = datetime.strptime("01/01/1940", "%d/%m/%Y")
            data_falecimento = data_final_cons - timedelta(days=365)
            data_sepultamento = data_falecimento + timedelta(days=2)
            data_inicio_cons = data_final_cons - timedelta(days=5 * 365)
            data_pagamento = data_inicio_cons

            return Sepultamento(
                cpf_falecido=cpf_falecido,
                nome_falecido=nome_falecido,
                data_nascimento=data_nascimento,
                data_falecimento=data_falecimento,
                causa_morte="Causas naturais",
                tumulo=Tumulo(
                    codigo=codigo_tumulo,
                    setor=setor,
                    numero=numero_tumulo,
                    tipo=TipoTumulo.Gaveteiro,
                    capacidade=2
                ),
                valor=2500.00,
                data_pagamento=data_pagamento,
                tipo_pagamento="PIX",
                responsavel="479.768.520-43",
                responsavel2="310.531.250-11",
                data_inicio_cons=data_inicio_cons,
                data_final_cons=data_final_cons,
                status=2,
                data_sepultamento=data_sepultamento,
                observacoes=observacoes
            )

        return [
            criar_sepultamento(
                cpf_falecido="794.880.230-40",
                nome_falecido="Carlos Pereira",
                codigo_tumulo=1,
                setor="A",
                numero_tumulo=12,
                data_final_cons=hoje - timedelta(days=90),
                observacoes=(
                    "Elegivel: concessao vencida ha 90 dias."
                )
            ),
            criar_sepultamento(
                cpf_falecido="529.982.247-25",
                nome_falecido="Maria Oliveira",
                codigo_tumulo=2,
                setor="A",
                numero_tumulo=18,
                data_final_cons=hoje - timedelta(days=31),
                observacoes=(
                    "Elegivel: concessao vencida ha 31 dias."
                )
            ),
            criar_sepultamento(
                cpf_falecido="111.444.777-35",
                nome_falecido="Joao Almeida",
                codigo_tumulo=3,
                setor="B",
                numero_tumulo=7,
                data_final_cons=hoje - timedelta(days=30),
                observacoes=(
                    "Elegivel no limite: data_final_cons + 30 dias ja chegou."
                )
            ),
            criar_sepultamento(
                cpf_falecido="123.456.789-09",
                nome_falecido="Ana Souza",
                codigo_tumulo=4,
                setor="B",
                numero_tumulo=21,
                data_final_cons=hoje - timedelta(days=15),
                observacoes=(
                    "Nao elegivel: concessao vencida ha apenas 15 dias."
                )
            ),
            criar_sepultamento(
                cpf_falecido="987.654.321-00",
                nome_falecido="Pedro Santos",
                codigo_tumulo=5,
                setor="C",
                numero_tumulo=4,
                data_final_cons=hoje + timedelta(days=60),
                observacoes=(
                    "Nao elegivel: concessao ainda nao venceu."
                )
            ),
            criar_sepultamento(
                cpf_falecido="390.533.447-05",
                nome_falecido="Helena Costa",
                codigo_tumulo=6,
                setor="C",
                numero_tumulo=30,
                data_final_cons=hoje - timedelta(days=365),
                observacoes=(
                    "Elegivel: concessao vencida ha aproximadamente 1 ano."
                )
            )
        ]

    def __auxiliar_busca_exumacao(self, codigo: int) -> Optional[Exumacao]:
        for exumacao in self.__exumacoes:
            if exumacao.codigo == codigo:
                return exumacao
            
        raise ValueError("Exumação selecionada não foi encontrada.")

    def __cpf_falecido_sepultamento(self, sepultamento: Sepultamento) -> str:
        falecido = sepultamento.falecido
        cpf = falecido.cpf

        return str(cpf)

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

    def __gerar_codigo_exumacao(self) -> int:
        maior_codigo = 0

        for exumacao in self.__exumacoes:
            codigo = exumacao.codigo

            if codigo > maior_codigo:
                maior_codigo = codigo

        return maior_codigo + 1

    def __obter_sepultamentos(self) -> list[Sepultamento]:
        # Fluxo real, para reativar depois:
        #
        # controlador_sepultamento = (
        #     self.__controlador_geral.controlador_sepultamento
        # )
        #
        # if controlador_sepultamento is None:
        #     raise ValueError(
        #         "Controlador de sepultamento não foi inicializado."
        #     )
        #
        # com @property da lista de sepultamentos:
        # return list(controlador_sepultamento.sepultamentos)
        #
        # se tiver um metodo de obter_sepultamentos():
        # return list(controlador_sepultamento.obter_sepultamentos())

        return list(self.__sepultamentos_teste)

    def __concessao_vencida_ha_mais_de_30_dias(
        self,
        sepultamento: Sepultamento
    ) -> bool:
        data_final = sepultamento.concessao.data_fim

        if data_final is None:
            return False

        data_minima_para_exumacao = data_final + timedelta(days=30)

        return datetime.now() >= data_minima_para_exumacao

    def __sepultamento_ja_possui_exumacao(
        self,
        sepultamento: Sepultamento
    ) -> bool:
        cpf_sepultamento = self.__cpf_falecido_sepultamento(sepultamento)

        for exumacao in self.__exumacoes:
            cpf_exumacao = self.__cpf_falecido_sepultamento(
                exumacao.sepultamento
            )

            if cpf_exumacao == cpf_sepultamento:
                return True

        return False

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

    def __formatar_tumulo(self, tumulo: Tumulo) -> str:
        return (
            f"Código {tumulo.codigo} | "
            f"Setor {tumulo.setor} | "
            f"Nº {tumulo.numero} | "
            f"{tumulo.tipo.name}"
        )

    def __formatar_sepultamento_para_tela(
        self,
        sepultamento: Sepultamento
    ) -> dict:
        falecido = sepultamento.falecido

        nome = falecido.nome
        cpf = falecido.cpf
        data_falecimento = self.__formatar_data(falecido.data_falecimento)
        data_sepultamento = self.__formatar_data(
            sepultamento.data_sepultamento
        )
        tumulo = self.__formatar_tumulo(sepultamento.tumulo)

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
            exumacao = self.__auxiliar_busca_exumacao(codigo)

            novos_dados = self.__tela_exumacao.pega_novos_dados_exumacao(
                self.__formatar_exumacao_para_tela(exumacao)
            )

            if novos_dados is None:
                return


            self.__validar_dados_exumacao(novos_dados)

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
            exumacao = self.__auxiliar_busca_exumacao(codigo)

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
