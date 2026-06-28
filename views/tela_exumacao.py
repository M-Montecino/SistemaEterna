import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from utils.funcoesAuxiliares import centralizar, mascara_data


class TelaExumacao:
    def __init__(self, master=None):
        self.__root = tk.Toplevel(master)
        self.__root.title("Gerenciamento de Exumações")
        self.__root.geometry("920x560")
        centralizar(self.__root)
        self.__root.minsize(820, 480)
        self.__root.protocol("WM_DELETE_WINDOW", self.__fechar_janela)
        self.__root.withdraw()

        cor_fundo = "#f4f6f9"
        cor_botao = "#68bced"
        cor_botao_voltar = "#777777"
        cor_texto_escuro = "#1f2937"
        cor_texto_secundario = "#6b7280"
        self.__root.configure(bg=cor_fundo)
        self.__cor_fundo = cor_fundo
        self.__cor_botao = cor_botao
        self.__cor_botao_voltar = cor_botao_voltar
        self.__cor_texto_escuro = cor_texto_escuro
        self.__cor_texto_secundario = cor_texto_secundario

        self.__evento = None
        self.__codigo_exumacao_selecionada = None
        self.__manter_foco_busca = False

        self.__montar_tela_principal()

    def __montar_tela_principal(self):
        cabecalho = tk.Frame(self.__root, bg=self.__cor_fundo)
        cabecalho.pack(fill="x", padx=12, pady=(12, 8))

        titulo = tk.Label(
            cabecalho,
            text="Gerenciamento de exumações",
            font=("Segoe UI", 18, "bold"),
            bg=self.__cor_fundo,
            fg=self.__cor_texto_escuro
        )
        titulo.pack(side="left")

        subtitulo = tk.Label(
            cabecalho,
            text="Controle e consulta das exumações",
            font=("Segoe UI", 10),
            bg=self.__cor_fundo,
            fg=self.__cor_texto_secundario
        )
        subtitulo.pack(side="left", padx=(10, 0), pady=(4, 0))

        botao_novo = tk.Button(
            cabecalho,
            text="Nova Exumação",
            width=16,
            height=2,
            bg=self.__cor_botao,
            fg="white",
            activebackground=self.__cor_botao,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: self.__selecionar_evento("cadastrar")
        )
        botao_novo.pack(side="right")

        frame_busca = tk.LabelFrame(
            self.__root,
            text="Buscar",
            bg=self.__cor_fundo,
            fg=self.__cor_texto_escuro,
            padx=8,
            pady=8
        )
        frame_busca.pack(fill="x", padx=12, pady=6)

        self.__entrada_busca = tk.Entry(
            frame_busca,
            relief="solid",
            bd=1
        )
        self.__entrada_busca.pack(side="left", fill="x", expand=True, padx=4, pady=4)
        self.__entrada_busca.bind(
            "<KeyRelease>",
            self.__acionar_filtro_busca
        )

        botao_limpar = tk.Button(
            frame_busca,
            text="Limpar",
            width=10,
            bg=self.__cor_botao_voltar,
            fg="white",
            activebackground=self.__cor_botao_voltar,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.__acionar_limpar_busca
        )
        botao_limpar.pack(side="left", padx=(4, 0), pady=4)

        frame_lista = tk.Frame(self.__root, bg=self.__cor_fundo)
        frame_lista.pack(fill="both", expand=True, padx=12, pady=6)

        self.__canvas = tk.Canvas(frame_lista, highlightthickness=0, bg=self.__cor_fundo)
        self.__barra_rolagem = tk.Scrollbar(
            frame_lista,
            orient="vertical",
            command=self.__canvas.yview
        )

        self.__frame_lista = tk.Frame(self.__canvas, bg=self.__cor_fundo)
        self.__janela_lista = self.__canvas.create_window(
            (0, 0),
            window=self.__frame_lista,
            anchor="nw"
        )

        self.__canvas.configure(yscrollcommand=self.__barra_rolagem.set)
        self.__canvas.pack(side="left", fill="both", expand=True)
        self.__barra_rolagem.pack(side="right", fill="y")

        self.__frame_lista.bind(
            "<Configure>",
            lambda evento: self.__canvas.configure(
                scrollregion=self.__canvas.bbox("all")
            )
        )
        self.__canvas.bind(
            "<Configure>",
            lambda evento: self.__canvas.itemconfigure(
                self.__janela_lista,
                width=evento.width
            )
        )

        rodape = tk.Frame(self.__root, bg=self.__cor_fundo)
        rodape.pack(fill="x", padx=12, pady=(6, 12))

        botao_voltar = tk.Button(
            rodape,
            text="Voltar ao Menu",
            width=16,
            height=2,
            bg=self.__cor_botao_voltar,
            fg="white",
            activebackground=self.__cor_botao_voltar,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.__fechar_janela
        )
        botao_voltar.pack(side="right")

        self.atualizar_lista_exumacoes([])

    def __acionar_filtro_busca(self, _evento=None):    # Tkinter precisa que exista parametro
        self.__manter_foco_busca = True
        self.__selecionar_evento("filtrar")

    def __focar_campo_busca(self):
        try:
            self.__entrada_busca.focus_force()
            self.__entrada_busca.icursor(tk.END)
        except tk.TclError:
            pass

        self.__manter_foco_busca = False

    def __criar_cabecalho_lista(self):
        colunas = [
            ("Código", 8),
            ("Sepultamento", 42),
            ("Data", 12),
            ("Destino", 22),
            ("Observações", 28),
            ("Ações", 18)
        ]

        for coluna, (texto, largura) in enumerate(colunas):
            label = tk.Label(
                self.__frame_lista,
                text=texto,
                font=("Arial", 10, "bold"),
                width=largura,
                anchor="w",
                relief="ridge",
                padx=4,
                pady=4,
                bg="#e5e7eb",
                fg=self.__cor_texto_escuro
            )
            label.grid(row=0, column=coluna, sticky="nsew")

        for coluna in range(len(colunas)):
            self.__frame_lista.grid_columnconfigure(coluna, weight=1)

    def atualizar_lista_exumacoes(self, exumacoes: list[dict]):
        for widget in self.__frame_lista.winfo_children():
            widget.destroy()

        self.__criar_cabecalho_lista()

        if not exumacoes:
            label = tk.Label(
                self.__frame_lista,
                text="Nenhuma exumação encontrada.",
                anchor="center",
                padx=8,
                pady=20
            )
            label.grid(row=1, column=0, columnspan=6, sticky="ew")
            return

        for linha, exumacao in enumerate(exumacoes, start=1):
            valores = [
                exumacao.get("codigo", ""),
                exumacao.get("sepultamento", ""),
                exumacao.get("data", ""),
                exumacao.get("destino", ""),
                exumacao.get("observacoes", "")
            ]
            larguras = [8, 42, 12, 22, 28]

            for coluna, valor in enumerate(valores):
                label = tk.Label(
                    self.__frame_lista,
                    text=str(valor),
                    width=larguras[coluna],
                    anchor="w",
                    relief="groove",
                    padx=4,
                    pady=4,
                    wraplength=300 if coluna in (1, 4) else 0,
                    justify="left",
                    bg="white",
                    fg=self.__cor_texto_escuro
                )
                label.grid(row=linha, column=coluna, sticky="nsew")

            frame_acoes = tk.Frame(
                self.__frame_lista,
                relief="groove",
                borderwidth=1,
                bg="white"
            )
            frame_acoes.grid(row=linha, column=5, sticky="nsew")

            codigo = exumacao.get("codigo")

            botao_alterar = tk.Button(
                frame_acoes,
                text="Alterar",
                width=8,
                command=lambda c=codigo: self.__selecionar_evento("alterar", c)
            )
            botao_alterar.pack(side="left", padx=3, pady=3)

            botao_remover = tk.Button(
                frame_acoes,
                text="Excluir",
                width=8,
                command=lambda c=codigo: self.__selecionar_evento("excluir", c)
            )
            botao_remover.pack(side="left", padx=3, pady=3)

    def __selecionar_evento(self, evento: str, codigo=None):
        self.__evento = evento
        self.__codigo_exumacao_selecionada = codigo
        self.__root.quit()

    def __acionar_limpar_busca(self):
        self.__entrada_busca.delete(0, tk.END)
        self.__manter_foco_busca = True
        self.__selecionar_evento("filtrar")

    def __converter_data(self, texto_data: str) -> datetime:
        texto_data = texto_data.strip()

        if texto_data == "" or texto_data == "dd/mm/aaaa":
            raise ValueError("Data é obrigatória.")

        try:
            data = datetime.strptime(texto_data, "%d/%m/%Y")
        except ValueError:
            raise ValueError(
                "Data inválida. Use o formato dd/mm/aaaa e informe uma data existente."
            )
        
        if data.date() < datetime.now().date():
            raise ValueError(
                "A data da exumação não pode ser anterior à data atual."
            )

        return data

    def pega_dados_busca(self) -> str:
        return self.__entrada_busca.get().strip()

    def limpa_busca(self):
        self.__entrada_busca.delete(0, tk.END)

    def pega_codigo_exumacao_selecionada(self):
        return self.__codigo_exumacao_selecionada

    def pega_dados_exumacao(self, sepultamentos_disponiveis: list[dict]):
        return self.__abre_formulario_exumacao(
            titulo="Cadastrar Exumação",
            sepultamentos_disponiveis=sepultamentos_disponiveis,
            exumacao=None,
            edicao=False
        )

    def pega_novos_dados_exumacao(self, exumacao: dict, somente_observacoes=False):
        return self.__abre_formulario_exumacao(
            titulo="Alterar Exumação",
            sepultamentos_disponiveis=[],
            exumacao=exumacao,
            edicao=True,
            somente_observacoes=somente_observacoes
        )

    def __abre_formulario_exumacao(
        self,
        titulo: str,
        sepultamentos_disponiveis: list[dict],
        exumacao: dict | None,
        edicao: bool,
        somente_observacoes: bool = False
    ):
        janela = tk.Toplevel(self.__root)
        janela.title(titulo)
        janela.geometry("650x430")
        janela.resizable(False, False)
        janela.transient(self.__root)
        janela.grab_set()

        resultado = {"dados": None}
        sepultamento_selecionado = {"objeto": None}

        frame = tk.Frame(janela)
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        tk.Label(
            frame,
            text=titulo,
            font=("Arial", 13, "bold")
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))

        tk.Label(frame, text="Sepultamento:").grid(
            row=1,
            column=0,
            sticky="nw",
            pady=4
        )

        entrada_sepultamento = tk.Entry(
            frame,
            width=62,
            state="disabled"
        )
        entrada_sepultamento.grid(row=1, column=1, sticky="w", pady=4)

        if edicao and exumacao is not None:
            entrada_sepultamento.configure(state="normal")
            entrada_sepultamento.delete(0, tk.END)
            entrada_sepultamento.insert(0, exumacao.get("sepultamento", ""))
            entrada_sepultamento.configure(state="disabled")

        botao_sepultamento = tk.Button(
            frame,
            text="Selecionar/Trocar",
            command=lambda: self.__selecionar_sepultamento_para_formulario(
                sepultamentos_disponiveis,
                entrada_sepultamento,
                sepultamento_selecionado
            )
        )
        botao_sepultamento.grid(row=1, column=2, padx=(8, 0), pady=4)

        if edicao:
            botao_sepultamento.configure(state="disabled")

        tk.Label(frame, text="Data:").grid(row=2, column=0, sticky="w", pady=4)
        entrada_data = tk.Entry(frame, width=20)
        entrada_data.grid(row=2, column=1, sticky="w", pady=4)
        entrada_data.bind("<KeyRelease>", mascara_data)

        if edicao and exumacao is not None:
            entrada_data.insert(0, exumacao.get("data", ""))
        else:
            entrada_data.insert(0, "dd/mm/aaaa")

        tk.Label(frame, text="Destino:").grid(row=3, column=0, sticky="w", pady=4)
        entrada_destino = tk.Entry(frame, width=62)
        entrada_destino.grid(row=3, column=1, columnspan=2, sticky="w", pady=4)

        if edicao and exumacao is not None:
            entrada_destino.insert(0, exumacao.get("destino", ""))

        tk.Label(frame, text="Observações:").grid(
            row=4,
            column=0,
            sticky="nw",
            pady=4
        )
        texto_observacoes = tk.Text(frame, width=47, height=6)
        texto_observacoes.grid(row=4, column=1, columnspan=2, sticky="w", pady=4)

        if edicao and exumacao is not None:
            texto_observacoes.insert("1.0", exumacao.get("observacoes", ""))
            
        if somente_observacoes:
            entrada_data.configure(state="disabled")
            entrada_destino.configure(state="disabled")

        frame_botoes = tk.Frame(frame)
        frame_botoes.grid(row=5, column=0, columnspan=3, sticky="e", pady=(18, 0))

        def salvar():
            try:
                observacoes = texto_observacoes.get("1.0", tk.END).strip()

                if somente_observacoes:
                    resultado["dados"] = {
                        "observacoes": observacoes
                    }

                    janela.destroy()
                    return
                
                if edicao and exumacao is not None:
                    sepultamento = None
                else:
                    sepultamento = sepultamento_selecionado["objeto"]

                    if sepultamento is None:
                        raise ValueError("Selecione um sepultamento.")

                data = self.__converter_data(entrada_data.get())
                destino = entrada_destino.get().strip()
                observacoes = texto_observacoes.get("1.0", tk.END).strip()

                if destino == "":
                    raise ValueError("Destino é obrigatório.")

                resultado["dados"] = {
                    "data": data,
                    "sepultamento": sepultamento,
                    "destino": destino,
                    "observacoes": observacoes
                }

                janela.destroy()

            except ValueError as erro:
                messagebox.showerror(
                    "Dados inválidos",
                    str(erro),
                    parent=janela
                )

        def cancelar():
            resultado["dados"] = None
            janela.destroy()

        tk.Button(frame_botoes, text="Salvar", width=12, command=salvar).pack(
            side="left",
            padx=4
        )
        tk.Button(frame_botoes, text="Cancelar", width=12, command=cancelar).pack(
            side="left",
            padx=4
        )

        janela.protocol("WM_DELETE_WINDOW", cancelar)
        self.__centralizar_janela(janela)
        janela.wait_window()

        return resultado["dados"]

    def __selecionar_sepultamento_para_formulario(
        self,
        sepultamentos_disponiveis: list[dict],
        entrada_sepultamento: tk.Entry,
        sepultamento_selecionado: dict
    ):
        selecionado = self.__abre_modal_selecao_sepultamento(
            sepultamentos_disponiveis
        )

        if selecionado is None:
            return

        sepultamento_selecionado["objeto"] = selecionado.get("objeto")

        entrada_sepultamento.configure(state="normal")
        entrada_sepultamento.delete(0, tk.END)
        entrada_sepultamento.insert(0, selecionado.get("texto", ""))
        entrada_sepultamento.configure(state="disabled")

    def __abre_modal_selecao_sepultamento(
        self,
        sepultamentos_disponiveis: list[dict]
    ):
        janela = tk.Toplevel(self.__root)
        janela.title("Selecionar Sepultamento")
        janela.geometry("680x420")
        janela.resizable(False, False)
        janela.transient(self.__root)
        janela.grab_set()

        resultado = {"sepultamento": None}
        itens_visiveis = {"lista": list(sepultamentos_disponiveis)}

        frame = tk.Frame(janela)
        frame.pack(fill="both", expand=True, padx=14, pady=14)

        tk.Label(
            frame,
            text="Selecione um sepultamento elegivel:",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 8))

        entrada_filtro = tk.Entry(frame)
        entrada_filtro.pack(fill="x", pady=(0, 8))

        frame_lista = tk.Frame(frame)
        frame_lista.pack(fill="both", expand=True)

        barra_rolagem = tk.Scrollbar(frame_lista)
        barra_rolagem.pack(side="right", fill="y")

        listbox = tk.Listbox(
            frame_lista,
            yscrollcommand=barra_rolagem.set,
            height=12
        )
        listbox.pack(side="left", fill="both", expand=True)
        barra_rolagem.config(command=listbox.yview)

        def atualizar_lista():
            filtro = entrada_filtro.get().strip().lower()
            listbox.delete(0, tk.END)

            if filtro == "":
                itens_visiveis["lista"] = list(sepultamentos_disponiveis)
            else:
                itens_visiveis["lista"] = [
                    item
                    for item in sepultamentos_disponiveis
                    if filtro in item.get("texto", "").lower()
                ]

            for item in itens_visiveis["lista"]:
                listbox.insert(tk.END, item.get("texto", ""))

        def confirmar():
            selecao = listbox.curselection()

            if not selecao:
                messagebox.showwarning(
                    "Seleção obrigatória",
                    "Selecione um sepultamento.",
                    parent=janela
                )
                return

            indice = selecao[0]
            resultado["sepultamento"] = itens_visiveis["lista"][indice]
            janela.destroy()

        def cancelar():
            resultado["sepultamento"] = None
            janela.destroy()

        entrada_filtro.bind("<KeyRelease>", lambda evento: atualizar_lista())
        listbox.bind("<Double-Button-1>", lambda evento: confirmar())

        frame_botoes = tk.Frame(frame)
        frame_botoes.pack(fill="x", pady=(10, 0))

        tk.Button(
            frame_botoes,
            text="Selecionar",
            width=12,
            command=confirmar
        ).pack(side="right", padx=4)
        tk.Button(
            frame_botoes,
            text="Cancelar",
            width=12,
            command=cancelar
        ).pack(side="right", padx=4)

        atualizar_lista()

        if listbox.size() > 0:
            listbox.selection_set(0)

        janela.protocol("WM_DELETE_WINDOW", cancelar)
        self.__centralizar_janela(janela)
        janela.wait_window()

        return resultado["sepultamento"]

    def confirma_exclusao_exumacao(self, exumacao: dict) -> bool:
        janela = tk.Toplevel(self.__root)
        janela.title("Remover Exumação")
        janela.geometry("580x330")
        janela.resizable(False, False)
        janela.transient(self.__root)
        janela.grab_set()

        resultado = {"confirmou": False}

        frame = tk.Frame(janela)
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        tk.Label(
            frame,
            text="Confirma a exclusão da exumação abaixo?",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 12))

        dados = [
            ("Código", exumacao.get("codigo", "")),
            ("Sepultamento", exumacao.get("sepultamento", "")),
            ("Data", exumacao.get("data", "")),
            ("Destino", exumacao.get("destino", "")),
            ("Observações", exumacao.get("observacoes", ""))
        ]

        for rotulo, valor in dados:
            linha = tk.Frame(frame)
            linha.pack(fill="x", pady=2)

            tk.Label(
                linha,
                text=f"{rotulo}:",
                width=14,
                anchor="w",
                font=("Arial", 10, "bold")
            ).pack(side="left")

            tk.Label(
                linha,
                text=str(valor),
                anchor="w",
                wraplength=400,
                justify="left"
            ).pack(side="left", fill="x", expand=True)

        frame_botoes = tk.Frame(frame)
        frame_botoes.pack(fill="x", pady=(16, 0))

        def confirmar():
            resultado["confirmou"] = True
            janela.destroy()

        def cancelar():
            resultado["confirmou"] = False
            janela.destroy()

        tk.Button(frame_botoes, text="Sim", width=12, command=confirmar).pack(
            side="right",
            padx=4
        )
        tk.Button(frame_botoes, text="Não", width=12, command=cancelar).pack(
            side="right",
            padx=4
        )

        janela.protocol("WM_DELETE_WINDOW", cancelar)
        self.__centralizar_janela(janela)
        janela.wait_window()

        return resultado["confirmou"]

    def tela_opcoes(self):
        self.__evento = None
        self.__root.deiconify()
        self.__root.grab_set()
        
        if self.__manter_foco_busca:
            self.__root.after_idle(self.__focar_campo_busca)
            
        self.__root.mainloop()

        try:
            self.__root.grab_release()
        except tk.TclError:
            pass

        if self.__evento is None:
            self.__evento = "voltar"

        if self.__evento == "voltar":
            self.__root.withdraw()

        return self.__evento

    def __fechar_janela(self):
        self.__selecionar_evento("voltar")

    def mostra_mensagem(self, mensagem):
        messagebox.showinfo("Mensagem", mensagem, parent=self.__root)

    def __centralizar_janela(self, janela: tk.Toplevel):
        janela.update_idletasks()

        largura = janela.winfo_width()
        altura = janela.winfo_height()

        if self.__root.winfo_viewable():
            x = self.__root.winfo_rootx() + (self.__root.winfo_width() // 2) - (largura // 2)
            y = self.__root.winfo_rooty() + (self.__root.winfo_height() // 2) - (altura // 2)
        else:
            x = (janela.winfo_screenwidth() // 2) - (largura // 2)
            y = (janela.winfo_screenheight() // 2) - (altura // 2)

        janela.geometry(f"+{x}+{y}")
