import tkinter as tk

from tkinter import (
    messagebox,
    simpledialog
)

from datetime import datetime


class TelaSepultamento:

    def __init__(
        self,
        master=None
    ):
        self.__root = tk.Toplevel(master)
        self.__root.title("Sepultamento")
        self.__root.geometry("350x450")
        self.__root.resizable(
            False,
            False)
        self.__root.protocol(
            "WM_DELETE_WINDOW",
            self.__fechar_janela
        )
        self.__root.transient(master)
        self.__root.withdraw()
        self.__opcao = None
        titulo = tk.Label(
            self.__root,
            text="SEPULTAMENTO",
            font=("Arial", 16, "bold")
        )

        titulo.pack(pady=10)

        botoes = [
            ("Cadastrar Sepultamento", 1),
            ("Alterar Sepultamento", 2),
            ("Excluir Sepultamento", 3),
            ("Listar Sepultamentos", 4),
            ("Buscar Sepultamento", 5),
            ("Voltar ao Menu", 0)
        ]

        for texto, valor in botoes:
            botao = tk.Button(
                self.__root,
                text=texto,
                width=25,
                height=2,
                command=lambda v=valor:
                    self.__selecionar_opcao(v)
            )
            botao.pack(pady=5)

    def pega_dados_sepultamento(self):
        janela_cadastro = tk.Toplevel(self.__root)
        janela_cadastro.title('Cadastro')
        janela_cadastro.geometry("500x550")

        dados = {}

        tk.Label(janela_cadastro, text='CPF').place(x=0, y=0)
        cpf_falecido = tk.Entry(janela_cadastro)
        cpf_falecido.place(x=190, y=0)

        tk.Label(janela_cadastro, text='Nome').place(x=0, y=30)
        nome_falecido = tk.Entry(janela_cadastro, width=30)
        nome_falecido.place(x=190, y=30)

        tk.Label(
            janela_cadastro,
            text='Data nascimento (dd/mm/aaaa)'
        ).place(x=0, y=60)
        nascimento_str = tk.Entry(janela_cadastro)
        nascimento_str.place(x=190, y=60)

        tk.Label(
            janela_cadastro,
            text='Data falecimento (dd/mm/aaaa)'
        ).place(x=0, y=90)
        falecimento_str = tk.Entry(janela_cadastro)
        falecimento_str.place(x=190, y=90)

        tk.Label(
            janela_cadastro,
            text='Causa morte'
        ).place(x=0, y=120)
        causa_morte = tk.Entry(janela_cadastro, width=30)
        causa_morte.place(x=190, y=120)

        tk.Label(
            janela_cadastro,
            text='Túmulo'
        ).place(x=0, y=150)
        tumulo = tk.Entry(janela_cadastro)
        tumulo.place(x=190, y=150)

        tk.Label(
            janela_cadastro,
            text='Valor pagamento'
        ).place(x=0, y=180)
        valor_pagamento = tk.Entry(janela_cadastro)
        valor_pagamento.place(x=190, y=180)

        tk.Label(
            janela_cadastro,
            text='Data pagamento (dd/mm/aaaa)'
        ).place(x=0, y=210)
        pagamento_str = tk.Entry(janela_cadastro)
        pagamento_str.place(x=190, y=210)

        tk.Label(
            janela_cadastro,
            text='Tipo pagamento'
        ).place(x=0, y=240)
        tipo_pagamento = tk.Entry(janela_cadastro)
        tipo_pagamento.place(x=190, y=240)

        tk.Label(
            janela_cadastro,
            text='Responsável 1'
        ).place(x=0, y=270)
        responsavel = tk.Entry(janela_cadastro)
        responsavel.place(x=190, y=270)

        tk.Label(
            janela_cadastro,
            text='Responsável 2'
        ).place(x=0, y=300)
        responsavel2 = tk.Entry(janela_cadastro)
        responsavel2.place(x=190, y=300)

        tk.Label(
            janela_cadastro,
            text='Início concessão (dd/mm/aaaa)'
        ).place(x=0, y=330)
        inicio_cons_str = tk.Entry(janela_cadastro)
        inicio_cons_str.place(x=190, y=330)

        tk.Label(
            janela_cadastro,
            text='Final concessão (dd/mm/aaaa)'
        ).place(x=0, y=360)
        final_cons_str = tk.Entry(janela_cadastro)
        final_cons_str.place(x=190, y=360)

        tk.Label(
            janela_cadastro,
            text='Status (1-Ativa / 2-Carência / 3-Vencida)'
        ).place(x=0, y=390)

        status = tk.Entry(janela_cadastro)
        status.place(x=250, y=390)

        tk.Label(
            janela_cadastro,
            text='Data sepultamento (dd/mm/aaaa)'
        ).place(x=0, y=420)

        sepultamento_str = tk.Entry(janela_cadastro)
        sepultamento_str.place(x=190, y=420)

        tk.Label(
            janela_cadastro,
            text='Observações'
        ).place(x=0, y=450)

        observacoes = tk.Entry(
            janela_cadastro,
            width=35
        )

        observacoes.place(x=190, y=450)

        def confirmar():
            dados["cpf_falecido"] = cpf_falecido.get()

            dados["nome_falecido"] = nome_falecido.get()

            dados["data_nascimento"] = datetime.strptime(
                nascimento_str.get(),
                "%d/%m/%Y"
            )

            dados["data_falecimento"] = datetime.strptime(
                falecimento_str.get(),
                "%d/%m/%Y"
            )

            dados["causa_morte"] = causa_morte.get()

            dados["tumulo"] = tumulo.get()

            dados["valor_pagamento"] = float(
                valor_pagamento.get()
            )

            dados["data_pagamento"] = datetime.strptime(
                pagamento_str.get(),
                "%d/%m/%Y"
            )

            dados["tipo_pagamento"] = tipo_pagamento.get()

            dados["responsavel"] = responsavel.get()

            dados["responsavel2"] = responsavel2.get()

            dados["data_inicio_cons"] = datetime.strptime(
                inicio_cons_str.get(),
                "%d/%m/%Y"
            )

            dados["data_final_cons"] = datetime.strptime(
                final_cons_str.get(),
                "%d/%m/%Y"
            )

            dados["status"] = int(status.get())

            dados["data_sepultamento"] = datetime.strptime(
                sepultamento_str.get(),
                "%d/%m/%Y"
            )

            dados["observacoes"] = observacoes.get()

            janela_cadastro.destroy()

        botao = tk.Button(
            janela_cadastro,
            text="Confirmar",
            command=confirmar
        )

        botao.place(x=190, y=490)

        janela_cadastro.wait_window()

        return dados

    def pega_cpf_alteracao(self):
        return simpledialog.askstring("Alterar", "CPF do falecido:")

    def pega_novas_observacoes(self):
        return simpledialog.askstring(
            "Alterar", "Novas observações:")

    def pega_cpf_exclusao(self):
        return simpledialog.askstring("Excluir", "CPF do falecido:")

    def pega_cpf_busca(self):
        return simpledialog.askstring("Buscar", "CPF do falecido:")

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