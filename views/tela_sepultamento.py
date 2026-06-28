import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from utils.funcoesAuxiliares import (
    centralizar,
    criar_botao_confirmacao,
    criar_entrada_estilizada,
    criar_popup_modal,
    mascara_data,
    pedir_dado,
)


class TelaSepultamento:
    def __init__(self,master=None):
        self.__root = tk.Toplevel(master)
        self.__root.title("Sepultamento")
        self.__root.geometry("400x600")
        centralizar(self.__root)
        self.__root.resizable(False, False)
        self.__root.protocol("WM_DELETE_WINDOW", self.__fechar_janela)
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
            text="SEPULTAMENTO",
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
            ("Cadastrar Sepultamento", 1),
            ("Alterar Sepultamento", 2),
            ("Excluir Sepultamento", 3),
            ("Listar Sepultamentos", 4),
            ("Buscar Sepultamento", 5),
            ("Voltar ao Menu", 0)
        ]

        for texto, valor in botoes:

            cor = COR_BOTAO if valor != 0 else COR_BOTAO_VOLTAR

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
#Rodapé

        rodape = tk.Label(
        self.__root,
        text="Sistema de Gerenciamento de Cemitério",
        font=("Segoe UI", 8),
        bg=COR_FUNDO,
        fg="#9ca3af"
        )
        rodape.pack(pady=(15, 10))

#Funções
    def pega_dados_sepultamento(self):
        janela, container = criar_popup_modal(
            self.__root,
            "Cadastro de Sepultamento",
            "Preencha os dados do sepultamento",
            largura=520,
            altura=640
        )

        dados = None

        cpf_falecido = criar_entrada_estilizada(container, "CPF do falecido")
        nome_falecido = criar_entrada_estilizada(container, "Nome do falecido")
        nascimento_str = criar_entrada_estilizada(container, "Data de nascimento (DD/MM/AAAA)")
        nascimento_str.bind("<KeyRelease>", mascara_data)
        falecimento_str = criar_entrada_estilizada(container, "Data de falecimento (DD/MM/AAAA)")
        falecimento_str.bind("<KeyRelease>", mascara_data)
        causa_morte = criar_entrada_estilizada(container, "Causa da morte")
        tumulo = criar_entrada_estilizada(container, "Túmulo")
        valor = criar_entrada_estilizada(container, "Valor do pagamento")
        pagamento_str = criar_entrada_estilizada(container, "Data do pagamento (DD/MM/AAAA)")
        pagamento_str.bind("<KeyRelease>", mascara_data)

        tk.Label(container, text="Tipo de pagamento", bg="#f4f6f9", fg="#1f2937").pack(anchor="w", pady=(8, 2))
        tipo_pagamento = ttk.Combobox(container, values=[1, 2, 3], state="readonly", width=28)
        tipo_pagamento.set(1)
        tipo_pagamento.pack(fill="x", pady=(2, 8))

        responsavel = criar_entrada_estilizada(container, "Responsável 1")
        responsavel2 = criar_entrada_estilizada(container, "Responsável 2")
        inicio_cons_str = criar_entrada_estilizada(container, "Início da concessão (DD/MM/AAAA)")
        inicio_cons_str.bind("<KeyRelease>", mascara_data)
        final_cons_str = criar_entrada_estilizada(container, "Final da concessão (DD/MM/AAAA)")
        final_cons_str.bind("<KeyRelease>", mascara_data)

        tk.Label(container, text="Status (1-Ativa / 2-Carência / 3-Vencida)", bg="#f4f6f9", fg="#1f2937").pack(anchor="w", pady=(8, 2))
        status = ttk.Combobox(container, values=[1, 2, 3], state="readonly", width=28)
        status.set(1)
        status.pack(fill="x", pady=(2, 8))

        sepultamento_str = criar_entrada_estilizada(container, "Data do sepultamento (DD/MM/AAAA)")
        sepultamento_str.bind("<KeyRelease>", mascara_data)
        observacoes = criar_entrada_estilizada(container, "Observações")

        def confirmar():
            nonlocal dados
            try:
                dados = {
                    "cpf_falecido": cpf_falecido.get().strip() or None,
                    "nome_falecido": nome_falecido.get().strip() or None,
                    "data_nascimento": datetime.strptime(nascimento_str.get(), "%d/%m/%Y") if nascimento_str.get() else None,
                    "data_falecimento": datetime.strptime(falecimento_str.get(), "%d/%m/%Y") if falecimento_str.get() else None,
                    "causa_morte": causa_morte.get().strip() or None,
                    "tumulo": tumulo.get().strip() or None,
                    "valor": float(valor.get().strip()) if valor.get().strip() else None,
                    "data_pagamento": datetime.strptime(pagamento_str.get(), "%d/%m/%Y") if pagamento_str.get() else None,
                    "tipo_pagamento": tipo_pagamento.get(),
                    "responsavel": responsavel.get().strip() or None,
                    "responsavel2": responsavel2.get().strip() or None,
                    "data_inicio_cons": datetime.strptime(inicio_cons_str.get(), "%d/%m/%Y") if inicio_cons_str.get() else None,
                    "data_final_cons": datetime.strptime(final_cons_str.get(), "%d/%m/%Y") if final_cons_str.get() else None,
                    "status": int(status.get()) if status.get() else None,
                    "data_sepultamento": datetime.strptime(sepultamento_str.get(), "%d/%m/%Y") if sepultamento_str.get() else None,
                    "observacoes": observacoes.get().strip() or None,
                }
            except ValueError:
                dados = None
            janela.destroy()

        criar_botao_confirmacao(container, confirmar)
        janela.protocol("WM_DELETE_WINDOW", lambda: janela.destroy())
        janela.bind("<Return>", lambda event: confirmar())
        janela.wait_window()

        return dados

    def pega_novos_dados_sepultamento(self):
        janela, container = criar_popup_modal(
            self.__root,
            "Alterar Sepultamento",
            "Atualize apenas os campos desejados",
            largura=460,
            altura=420
        )

        dados = {}

        tumulo = criar_entrada_estilizada(container, "Novo túmulo")
        data_pagamento = criar_entrada_estilizada(container, "Nova data de pagamento (DD/MM/AAAA)")
        data_pagamento.bind("<KeyRelease>", mascara_data)

        tk.Label(container, text="Novo tipo de pagamento", bg="#f4f6f9", fg="#1f2937").pack(anchor="w", pady=(8, 2))
        tipo_pagamento = ttk.Combobox(container, values=["Débito", "Crédito", "Pix"], state="readonly", width=28)
        tipo_pagamento.pack(fill="x", pady=(2, 8))

        data_final = criar_entrada_estilizada(container, "Nova data final de concessão (DD/MM/AAAA)")
        data_final.bind("<KeyRelease>", mascara_data)

        tk.Label(container, text="Novo status", bg="#f4f6f9", fg="#1f2937").pack(anchor="w", pady=(8, 2))
        status = ttk.Combobox(container, values=["ATIVA", "CARENCIA", "VENCIDA"], state="readonly", width=28)
        status.pack(fill="x", pady=(2, 8))

        observacoes = criar_entrada_estilizada(container, "Novas observações")

        def confirmar():
            dados["tumulo"] = int(tumulo.get().strip()) if tumulo.get().strip() else None
            dados["data_pagamento"] = datetime.strptime(data_pagamento.get(), "%d/%m/%Y") if data_pagamento.get() else None
            dados["tipo_pagamento"] = tipo_pagamento.get() if tipo_pagamento.get() else None
            dados["data_final_cons"] = datetime.strptime(data_final.get(), "%d/%m/%Y") if data_final.get() else None
            dados["status"] = status.get() if status.get() else None
            dados["observacoes"] = observacoes.get().strip() or None
            janela.destroy()

        criar_botao_confirmacao(container, confirmar)
        janela.protocol("WM_DELETE_WINDOW", lambda: janela.destroy())
        janela.bind("<Return>", lambda event: confirmar())
        janela.wait_window()

        return dados

    def pega_cpf_alteracao(self):
        return pedir_dado(
            self.__root,
            "Alterar Sepultamento",
            "CPF do falecido:",
            tipo="texto"
        )

    def pega_cpf_exclusao(self):
        return pedir_dado(
            self.__root,
            "Excluir Sepultamento",
            "CPF do falecido:",
            tipo="texto"
        )
        
    def __selecionar_opcao(
        self, valor):
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

    def mostra_mensagem(
        self,
        mensagem
    ):

        messagebox.showinfo(
            "Mensagem",
            mensagem
        )