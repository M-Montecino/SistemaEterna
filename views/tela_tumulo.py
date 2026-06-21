import tkinter as tk
from tkinter import ttk, simpledialog, messagebox


class TelaTumulo:

    def __init__(self, master=None):
        self.__root = tk.Toplevel(master)
        self.__root.title("Túmulos")
        self.__root.geometry("350x450")
        self.__root.resizable(False, False)

        self.__root.protocol(
            "WM_DELETE_WINDOW",
            self.__fechar_janela
        )

        self.__root.transient(master)
        self.__root.withdraw()

        self.__opcao = None

        titulo = tk.Label(
            self.__root,
            text="TÚMULOS",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        botoes = [
            ("Cadastrar Túmulo", 1),
            ("Alterar Túmulo", 2),
            ("Excluir Túmulo", 3),
            ("Listar Túmulos", 4),
            ("Buscar Túmulo", 5),
            ("Voltar ao Menu", 0)
        ]

        for texto, valor in botoes:
            tk.Button(
                self.__root,
                text=texto,
                width=25,
                height=2,
                command=lambda v=valor:
                    self.__selecionar_opcao(v)
            ).pack(pady=5)

    def pega_dados_tumulo(self):
        janela = tk.Toplevel(self.__root)
        janela.title("Cadastro de Túmulo")
        janela.geometry("450x300")

        dados = None

        tk.Label(janela, text="Código").place(x=0, y=0)
        codigo = tk.Entry(janela)
        codigo.place(x=150, y=0)

        tk.Label(janela, text="Setor").place(x=0, y=40)
        setor = tk.Entry(janela)
        setor.place(x=150, y=40)

        tk.Label(janela, text="Número").place(x=0, y=80)
        numero = tk.Entry(janela)
        numero.place(x=150, y=80)

        tk.Label(
            janela,
            text="Tipo (1-Cova / 2-Cripta / 3-Gaveteiro)"
        ).place(x=0, y=120)

        tipo = ttk.Combobox(
            janela,
            values=[1, 2, 3],
            state="readonly"
        )

        tipo.place(x=260, y=120)

        tk.Label(janela, text="Capacidade").place(x=0, y=160)
        capacidade = tk.Entry(janela)
        capacidade.place(x=150, y=160)

        def confirmar():
            nonlocal dados

            dados = {
                "codigo": int(codigo.get()),
                "setor": setor.get(),
                "numero": int(numero.get()),
                "tipo": int(tipo.get()),
                "capacidade": int(capacidade.get())
            }

            janela.destroy()

        tk.Button(
            janela,
            text="Confirmar",
            command=confirmar
        ).place(x=150, y=220)

        janela.protocol(
            "WM_DELETE_WINDOW",
            lambda: janela.destroy()
        )

        janela.wait_window()

        return dados

    def pega_novos_dados_tumulo(self):
        janela = tk.Toplevel(self.__root)
        janela.title("Alterar Túmulo")
        janela.geometry("450x250")

        dados = {}

        tk.Label(janela, text="Novo setor").place(x=0, y=0)
        setor = tk.Entry(janela)
        setor.place(x=150, y=0)

        tk.Label(janela, text="Novo número").place(x=0, y=40)
        numero = tk.Entry(janela)
        numero.place(x=150, y=40)

        tk.Label(
            janela,
            text="Novo tipo (1-Cova / 2-Cripta / 3-Gaveteiro)"
        ).place(x=0, y=80)

        tipo = ttk.Combobox(
            janela,
            values=[1, 2, 3],
            state="readonly"
        )

        tipo.place(x=260, y=80)

        tk.Label(janela, text="Nova capacidade").place(x=0, y=120)
        capacidade = tk.Entry(janela)
        capacidade.place(x=150, y=120)

        def confirmar():
            dados["setor"] = (
                setor.get()
                if setor.get()
                else None
            )

            dados["numero"] = (
                int(numero.get())
                if numero.get()
                else None
            )

            dados["tipo"] = (
                int(tipo.get())
                if tipo.get()
                else None
            )

            dados["capacidade"] = (
                int(capacidade.get())
                if capacidade.get()
                else None
            )

            janela.destroy()

        tk.Button(
            janela,
            text="Confirmar",
            command=confirmar
        ).place(x=150, y=180)

        janela.protocol(
            "WM_DELETE_WINDOW",
            lambda: janela.destroy()
        )

        janela.wait_window()

        return dados

    def alterar_tumulo(self):
        return simpledialog.askinteger(
            "Alterar",
            "Código do túmulo:"
        )

    def excluir_tumulo(self):
        return simpledialog.askinteger(
            "Excluir",
            "Código do túmulo:"
        )

    def buscar_tumulo(self):
        return simpledialog.askinteger(
            "Buscar",
            "Código do túmulo:"
        )

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