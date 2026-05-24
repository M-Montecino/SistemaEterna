import tkinter as tk
from tkinter import messagebox

class TelaLogin:
    def __init__(self, master=None):
        if master is None:
            self.__root = tk.Tk()
        else:
            self.__root = tk.Toplevel(master)
            self.__root.transient(master)

        self.__root.title("Login")
        self.__root.geometry("320x220")
        self.__root.resizable(False, False)
        self.__root.protocol("WM_DELETE_WINDOW", self.__fechar_janela)

        if master is not None:
            self.__root.withdraw()

        self.__cpf_var = tk.StringVar()
        self.__senha_var = tk.StringVar()
        self.__opcao = None

        titulo = tk.Label(
            self.__root,
            text="LOGIN",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        frame_campos = tk.Frame(self.__root)
        frame_campos.pack(pady=5, padx=20, fill="x")

        label_cpf = tk.Label(frame_campos, text="CPF:", anchor="w")
        label_cpf.pack(fill="x")
        entrada_cpf = tk.Entry(frame_campos, textvariable=self.__cpf_var)
        entrada_cpf.pack(fill="x", pady=5)

        label_senha = tk.Label(frame_campos, text="Senha:", anchor="w")
        label_senha.pack(fill="x")
        entrada_senha = tk.Entry(
            frame_campos,
            textvariable=self.__senha_var,
            show="*"
        )
        entrada_senha.pack(fill="x", pady=5)

        frame_botoes = tk.Frame(self.__root)
        frame_botoes.pack(pady=15)

        botao_login = tk.Button(
            frame_botoes,
            text="Entrar",
            width=12,
            command=self.__realizar_login
        )
        botao_login.pack(side="left", padx=5)

        botao_cancelar = tk.Button(
            frame_botoes,
            text="Cancelar",
            width=12,
            command=self.__cancelar
        )
        botao_cancelar.pack(side="left", padx=5)

    def __realizar_login(self):
        self.__opcao = 1
        self.__root.quit()

    def __cancelar(self):
        self.__opcao = 0
        self.__root.quit()

    def __fechar_janela(self):
        self.__opcao = 0
        self.__root.quit()

    def tela_login(self):
        self.__cpf_var.set("")
        self.__senha_var.set("")
        self.__opcao = None

        self.__root.deiconify()
        self.__root.grab_set()
        self.__root.mainloop()
        self.__root.grab_release()
        self.__root.withdraw()

        if self.__opcao is None:
            self.__opcao = 0

        return self.__opcao

    def pega_dados_login(self):
        return {
            "cpf": self.__cpf_var.get(),
            "senha": self.__senha_var.get()
        }

    @property
    def root(self):
        return self.__root

    def mostra_mensagem(self, mensagem):
        messagebox.showinfo("Mensagem", mensagem)
