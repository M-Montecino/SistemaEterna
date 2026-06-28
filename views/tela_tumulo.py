import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from utils.funcoesAuxiliares import (
    centralizar,
    criar_botao_confirmacao,
    criar_entrada_estilizada,
    criar_popup_modal,
    pedir_dado,
)


class TelaTumulo:
    def __init__(self, master=None):
        self.__root = tk.Toplevel(master)
        self.__root.title("Túmulos")
        self.__root.geometry("400x600")
        centralizar(self.__root)
        self.__root.resizable(False, False)
        self.__root.protocol("WM_DELETE_WINDOW",self.__fechar_janela)
        self.__root.withdraw()

        self.__opcao = None

        # Cores
        COR_FUNDO = "#f4f6f9"
        COR_BOTAO = "#68bced"
        COR_BOTAO_VOLTAR = "#777777"
        COR_TEXTO = "white"
        
        self.__root.configure(bg=COR_FUNDO)

#Títulos
        titulo = tk.Label(
            self.__root,
            text="TÚMULO",
            font=("Segoe UI", 20, "bold"),
            bg=COR_FUNDO,
            fg="#1f2937"
        )
        titulo.pack(pady=(25, 5))

        subtitulo = tk.Label(
            self.__root,
            text="Selecione uma opção",
            font=("Segoe UI", 10),
            bg=COR_FUNDO,
            fg="#6b7280"
        )
        subtitulo.pack(pady=(0, 20))

        frame = tk.Frame(self.__root, bg=COR_FUNDO)
        frame.pack(fill="both", expand=True)

#Botões
        botoes = [
            ("Cadastrar Túmulo", 1),
            ("Alterar Túmulo", 2),
            ("Excluir Túmulo", 3),
            ("Listar Túmulos", 4),
            ("Buscar Túmulo", 5),
            ("Relatório de Ocupação", 6),
            ("Voltar ao Menu", 0)
        ]

        for texto, valor in botoes:

            cor = COR_BOTAO if valor !=0 else COR_BOTAO_VOLTAR

            botao = tk.Button(
                frame,
                text=texto,
                font=("Segoe UI", 11, "bold"),
                width=28,
                height=2,
                bg=cor,
                fg=COR_TEXTO,
                activebackground=COR_BOTAO,
                activeforeground="white",
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda v=valor: self.__selecionar_opcao(v)
            )

            botao.pack(pady=7)
#rodapé

        rodape = tk.Label(
        self.__root,
        text="Sistema de Gerenciamento de Cemitério",
        font=("Segoe UI", 8),
        bg=COR_FUNDO,
        fg="#9ca3af"
        )
        rodape.pack(pady=(15, 10))

#funções
    def pega_dados_tumulo(self):
        janela, container = criar_popup_modal(
            self.__root,
            "Cadastro de Túmulo",
            "Preencha os dados do túmulo",
            largura=460,
            altura=400
        )

        codigo = criar_entrada_estilizada(container, "Código")
        setor = criar_entrada_estilizada(container, "Setor")
        numero = criar_entrada_estilizada(container, "Número")
        tk.Label(container, text="Tipo (1-Cova / 2-Cripta / 3-Gaveteiro)", bg="#f4f6f9", fg="#1f2937").pack(anchor="w", pady=(8, 2))
        tipo = ttk.Combobox(container, values=[1, 2, 3], state="readonly", width=28)
        tipo.set(1)
        tipo.pack(fill="x", pady=(2, 8))
        capacidade = criar_entrada_estilizada(container, "Capacidade")

        dados = None

        def confirmar():
            nonlocal dados
            try:
                dados = {
                    "codigo": int(codigo.get().strip()) if codigo.get().strip() else None,
                    "setor": setor.get().strip() or None,
                    "numero": int(numero.get().strip()) if numero.get().strip() else None,
                    "tipo": int(tipo.get()) if tipo.get() else None,
                    "capacidade": int(capacidade.get().strip()) if capacidade.get().strip() else None,
                }
            except ValueError:
                dados = {
                    "codigo": None,
                    "setor": setor.get().strip() or None,
                    "numero": None,
                    "tipo": None,
                    "capacidade": None,
                }
            janela.destroy()

        criar_botao_confirmacao(container, confirmar)
        janela.protocol("WM_DELETE_WINDOW", lambda: janela.destroy())
        janela.bind("<Return>", lambda event: confirmar())
        janela.wait_window()

        return dados

    def pega_novos_dados_tumulo(self):
        janela, container = criar_popup_modal(
            self.__root,
            "Alterar Túmulo",
            "Atualize apenas os campos desejados",
            largura=460,
            altura=360
        )

        dados = {}

        setor = criar_entrada_estilizada(container, "Novo setor")
        numero = criar_entrada_estilizada(container, "Novo número")
        tk.Label(container, text="Novo tipo (1-Cova / 2-Cripta / 3-Gaveteiro)", bg="#f4f6f9", fg="#1f2937").pack(anchor="w", pady=(8, 2))
        tipo = ttk.Combobox(container, values=[1, 2, 3], state="readonly", width=28)
        tipo.set(1)
        tipo.pack(fill="x", pady=(2, 8))
        capacidade = criar_entrada_estilizada(container, "Nova capacidade")

        def confirmar():
            valor_numero = numero.get().strip()
            try:
                numero_convertido = int(valor_numero) if valor_numero else None
            except ValueError:
                numero_convertido = None

            valor_capacidade = capacidade.get().strip()
            try:
                capacidade_convertida = int(valor_capacidade) if valor_capacidade else None
            except ValueError:
                capacidade_convertida = None

            dados["setor"] = setor.get().strip() or None
            dados["numero"] = numero_convertido
            dados["tipo"] = int(tipo.get()) if tipo.get() else None
            dados["capacidade"] = capacidade_convertida
            janela.destroy()

        criar_botao_confirmacao(container, confirmar)
        janela.protocol("WM_DELETE_WINDOW", lambda: janela.destroy())
        janela.bind("<Return>", lambda event: confirmar())
        janela.wait_window()

        return dados

    def alterar_tumulo(self):
        return pedir_dado(
            self.__root,
            "Alterar Túmulo",
            "Código do túmulo:",
            tipo="inteiro"
        )

    def excluir_tumulo(self):
        return pedir_dado(
            self.__root,
            "Excluir Túmulo",
            "Código do túmulo:",
            tipo="inteiro"
        )

    def buscar_tumulo(self):
        return pedir_dado(
            self.__root,
            "Buscar Túmulo",
            "Código do túmulo:",
            tipo="inteiro"
        )
    
    def mostra_relatorio_ocupacao(self, relatorio):
        janela = tk.Toplevel(self.__root)
        janela.title("Relatório de Ocupação dos Túmulos")
        janela.geometry("850x400")

        colunas = (
            "codigo",
            "setor",
            "numero",
            "tipo",
            "capacidade",
            "ocupados",
            "vagas_livres",
            "status"
        )

        tabela = ttk.Treeview(
            janela,
            columns=colunas,
            show="headings"
        )

        tabela.heading("codigo", text="Código")
        tabela.heading("setor", text="Setor")
        tabela.heading("numero", text="Número")
        tabela.heading("tipo", text="Tipo")
        tabela.heading("capacidade", text="Capacidade")
        tabela.heading("ocupados", text="Ocupados")
        tabela.heading("vagas_livres", text="Vagas Livres")
        tabela.heading("status", text="Status")

        tabela.column("codigo", width=80, anchor="center")
        tabela.column("setor", width=80, anchor="center")
        tabela.column("numero", width=80, anchor="center")
        tabela.column("tipo", width=120, anchor="center")
        tabela.column("capacidade", width=100, anchor="center")
        tabela.column("ocupados", width=100, anchor="center")
        tabela.column("vagas_livres", width=120, anchor="center")
        tabela.column("status", width=120, anchor="center")

        for item in relatorio:
            tabela.insert(
                "",
                "end",
                values=(
                    item["codigo"],
                    item["setor"],
                    item["numero"],
                    item["tipo"],
                    item["capacidade"],
                    item["ocupados"],
                    item["vagas_livres"],
                    item["status"]
                )
            )

        tabela.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(
            janela,
            text="Fechar",
            command=janela.destroy
        ).pack(pady=10)

    def __selecionar_opcao(self, valor):
        self.__opcao = valor
        self.__root.quit()

    def tela_opcoes(self):
        self.__opcao = None

        self.__root.deiconify()
        self.__root.grab_set()

        self.__root.mainloop()

        self.__root.grab_release()
        self.__root.withdraw()

        if self.__opcao is None:
            self.__opcao = 0

        return self.__opcao

    def __fechar_janela(self):
        self.__opcao = 0
        self.__root.quit()

    def mostra_mensagem(self, mensagem):
        messagebox.showinfo(
            "Mensagem",
            mensagem
        )