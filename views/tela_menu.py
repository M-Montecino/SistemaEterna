import tkinter as tk
from tkinter import messagebox

class TelaMenu:
    def __init__(self, master=None):
        if master is None:
            self.__root = tk.Tk()
        else:
            self.__root = tk.Toplevel(master)
            self.__root.transient(master)

        self.__root.title("Sistema Eterna")
        self.__root.geometry("320x520")
        self.__root.resizable(False, False)
        self.__root.protocol("WM_DELETE_WINDOW", self.__fechar_janela)

        self.__opcao = None

        titulo = tk.Label(
            self.__root,
            text="MENU PRINCIPAL",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        botoes = [
            ("Manutenção", 1),
            ("Túmulo", 2),
            ("Sepultamento", 3),
            ("Responsável", 4),
            ("Usuário", 5),
            ("Exumação", 6),
            ("Logout", 7),
            ("Encerrar Sistema", 0)
        ]

        for texto, valor in botoes:
            botao = tk.Button(
                self.__root,
                text=texto,
                width=20,
                height=2,
                command=lambda v=valor: self.__selecionar_opcao(v)
            )

            botao.pack(pady=5)

    def __selecionar_opcao(self, valor):
        self.__opcao = valor
        self.__root.quit()

    def __fechar_janela(self):
        self.__opcao = 0
        self.__root.quit()

    def tela_opcoes(self):
        self.__opcao = None

        self.__root.mainloop()

        if self.__opcao is None:
            self.__opcao = 0

        return self.__opcao

    @property
    def root(self):
        return self.__root

    def mostra_mensagem(self, mensagem):
        messagebox.showinfo("Mensagem", mensagem)