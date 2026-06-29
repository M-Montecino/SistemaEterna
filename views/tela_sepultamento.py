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
    def __criar_area_scroll(self, container):
        canvas = tk.Canvas(container, bg="#f4f6f9", highlightthickness=0)
        barra = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=barra.set)

        barra.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        frame = tk.Frame(canvas, bg="#f4f6f9")
        item = canvas.create_window((0, 0), window=frame, anchor="nw")

        def ajustar_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(item, width=event.width if event else frame.winfo_width())

        frame.bind("<Configure>", ajustar_scroll)
        canvas.bind("<Configure>", ajustar_scroll)
        return frame

    def pega_dados_sepultamento(self):
        janela, container = criar_popup_modal(
            self.__root,
            "Cadastro de Sepultamento",
            "Preencha os dados do sepultamento",
            largura=520,
            altura=760
        )
        frame_form = self.__criar_area_scroll(container)

        dados = None

        cpf_falecido = criar_entrada_estilizada(frame_form, "CPF do falecido")
        nome_falecido = criar_entrada_estilizada(frame_form, "Nome do falecido")
        nascimento_str = criar_entrada_estilizada(frame_form, "Data de nascimento (DD/MM/AAAA)")
        nascimento_str.bind("<KeyRelease>", mascara_data)
        falecimento_str = criar_entrada_estilizada(frame_form, "Data de falecimento (DD/MM/AAAA)")
        falecimento_str.bind("<KeyRelease>", mascara_data)
        causa_morte = criar_entrada_estilizada(frame_form, "Causa da morte")
        tumulo = criar_entrada_estilizada(frame_form, "Túmulo")
        valor = criar_entrada_estilizada(frame_form, "Valor do pagamento")
        pagamento_str = criar_entrada_estilizada(frame_form, "Data do pagamento (DD/MM/AAAA)")
        pagamento_str.bind("<KeyRelease>", mascara_data)

        tk.Label(frame_form, text="Tipo de pagamento (1-Débito / 2-Crédito / 3-Pix)", bg="#f4f6f9", fg="#1f2937").pack(anchor="w", pady=(8, 2))
        tipo_pagamento = ttk.Combobox(frame_form, values=[1, 2, 3], state="readonly", width=28)
        tipo_pagamento.set(1)
        tipo_pagamento.pack(fill="x", pady=(2, 4))

        responsavel = criar_entrada_estilizada(frame_form, "Responsável 1")
        responsavel2 = criar_entrada_estilizada(frame_form, "Responsável 2")
        inicio_cons_str = criar_entrada_estilizada(frame_form, "Início da concessão (DD/MM/AAAA)")
        inicio_cons_str.bind("<KeyRelease>", mascara_data)
        final_cons_str = criar_entrada_estilizada(frame_form, "Final da concessão (DD/MM/AAAA)")
        final_cons_str.bind("<KeyRelease>", mascara_data)

        tk.Label(frame_form, text="Status (1-Ativa / 2-Carência / 3-Vencida)", bg="#f4f6f9", fg="#1f2937").pack(anchor="w", pady=(8, 2))
        status = ttk.Combobox(frame_form, values=[1, 2, 3], state="readonly", width=28)
        status.set(1)
        status.pack(fill="x", pady=(2, 4))

        sepultamento_str = criar_entrada_estilizada(frame_form, "Data do sepultamento (DD/MM/AAAA)")
        sepultamento_str.bind("<KeyRelease>", mascara_data)
        observacoes = criar_entrada_estilizada(frame_form, "Observações")

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

        criar_botao_confirmacao(frame_form, confirmar)
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
            altura=620
        )
        frame_form = self.__criar_area_scroll(container)

        dados = {}

        tumulo = criar_entrada_estilizada(frame_form, "Novo túmulo")
        data_pagamento = criar_entrada_estilizada(frame_form, "Nova data de pagamento (DD/MM/AAAA)")
        data_pagamento.bind("<KeyRelease>", mascara_data)

        tk.Label(frame_form, text="Novo tipo de pagamento", bg="#f4f6f9", fg="#1f2937").pack(anchor="w", pady=(8, 2))
        tipo_pagamento = ttk.Combobox(frame_form, values=["Débito", "Crédito", "Pix"], state="readonly", width=28)
        tipo_pagamento.pack(fill="x", pady=(2, 4))

        data_final = criar_entrada_estilizada(frame_form, "Nova data final de concessão (DD/MM/AAAA)")
        data_final.bind("<KeyRelease>", mascara_data)

        tk.Label(frame_form, text="Novo status", bg="#f4f6f9", fg="#1f2937").pack(anchor="w", pady=(8, 2))
        status = ttk.Combobox(frame_form, values=["ATIVA", "CARENCIA", "VENCIDA"], state="readonly", width=28)
        status.pack(fill="x", pady=(2, 4))

        observacoes = criar_entrada_estilizada(frame_form, "Novas observações")

        def confirmar():
            dados["tumulo"] = int(tumulo.get().strip()) if tumulo.get().strip() else None
            dados["data_pagamento"] = datetime.strptime(data_pagamento.get(), "%d/%m/%Y") if data_pagamento.get() else None
            dados["tipo_pagamento"] = tipo_pagamento.get() if tipo_pagamento.get() else None
            dados["data_final_cons"] = datetime.strptime(data_final.get(), "%d/%m/%Y") if data_final.get() else None
            dados["status"] = status.get() if status.get() else None
            dados["observacoes"] = observacoes.get().strip() or None
            janela.destroy()

        criar_botao_confirmacao(frame_form, confirmar)
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