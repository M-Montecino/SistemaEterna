import tkinter as tk
from tkinter import simpledialog, messagebox


class TelaResponsavel:

    def __init__(self, master=None):
        self.__root = tk.Toplevel(master)
        self.__root.title("Responsáveis")
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
            text="RESPONSÁVEIS",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        botoes = [
            ("Cadastrar Responsável", 1),
            ("Alterar Responsável", 2),
            ("Excluir Responsável", 3),
            ("Listar Responsáveis", 4),
            ("Buscar Responsável", 5),
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

    def pegar_dados_responsavel(self):
        janela = tk.Toplevel(self.__root)
        janela.title("Cadastro de Responsável")
        janela.geometry("450x320")

        dados = None

        tk.Label(janela, text="Nome").place(x=0, y=0)
        nome = tk.Entry(janela)
        nome.place(x=150, y=0)

        tk.Label(janela, text="CPF").place(x=0, y=40)
        cpf = tk.Entry(janela)
        cpf.place(x=150, y=40)

        tk.Label(janela, text="Telefone").place(x=0, y=80)
        telefone = tk.Entry(janela)
        telefone.place(x=150, y=80)

        tk.Label(janela, text="CEP").place(x=0, y=120)
        cep = tk.Entry(janela)
        cep.place(x=150, y=120)

        tk.Label(janela, text="Número").place(x=0, y=160)
        numero = tk.Entry(janela)
        numero.place(x=150, y=160)

        tk.Label(janela, text="Email").place(x=0, y=200)
        email = tk.Entry(janela)
        email.place(x=150, y=200)

        def confirmar():
            nonlocal dados

            dados = {
                "nome": nome.get(),
                "cpf": cpf.get(),
                "telefone": telefone.get(),
                "cep": cep.get(),
                "numero": int(numero.get()),
                "email": email.get()
            }

            janela.destroy()

        tk.Button(
            janela,
            text="Confirmar",
            command=confirmar
        ).place(x=170, y=260)

        janela.protocol(
            "WM_DELETE_WINDOW",
            lambda: janela.destroy()
        )

        janela.wait_window()

        return dados

    def pega_novos_dados_responsavel(self):
        janela = tk.Toplevel(self.__root)
        janela.title("Alterar Responsável")
        janela.geometry("450x320")

        dados = {}

        tk.Label(janela, text="Novo nome").place(x=0, y=0)
        nome = tk.Entry(janela)
        nome.place(x=150, y=0)

        tk.Label(janela, text="Novo telefone").place(x=0, y=40)
        telefone = tk.Entry(janela)
        telefone.place(x=150, y=40)

        tk.Label(janela, text="Novo CEP").place(x=0, y=80)
        cep = tk.Entry(janela)
        cep.place(x=150, y=80)

        tk.Label(janela, text="Novo número").place(x=0, y=120)
        numero = tk.Entry(janela)
        numero.place(x=150, y=120)

        tk.Label(janela, text="Novo email").place(x=0, y=160)
        email = tk.Entry(janela)
        email.place(x=150, y=160)

        def confirmar():
            dados["nome"] = (
                nome.get() if nome.get() else None
            )

            dados["telefone"] = (
                telefone.get() if telefone.get() else None
            )

            dados["cep"] = (
                cep.get() if cep.get() else None
            )

            dados["numero"] = (
                int(numero.get())
                if numero.get()
                else None
            )

            dados["email"] = (
                email.get() if email.get() else None
            )

            janela.destroy()

        tk.Button(
            janela,
            text="Confirmar",
            command=confirmar
        ).place(x=170, y=230)

        janela.protocol(
            "WM_DELETE_WINDOW",
            lambda: janela.destroy()
        )

        janela.wait_window()

        return dados

    def alterar_responsavel(self):
        return simpledialog.askstring(
            "Alterar",
            "CPF do responsável:"
        )

    def excluir_responsavel(self):
        return simpledialog.askstring(
            "Excluir",
            "CPF do responsável:"
        )

    def buscar_responsavel(self):
        return simpledialog.askstring(
            "Buscar",
            "CPF do responsável:"
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