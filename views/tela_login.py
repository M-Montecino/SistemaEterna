import tkinter as tk
from tkinter import messagebox
from utils.funcoesAuxiliares import centralizar

class TelaLogin:
    def __init__(self, master=None):
        if master is None:
            self.__root = tk.Tk()
        else:
            self.__root = tk.Toplevel(master)
            self.__root.transient(master)

        self.__root.title("Login")
        self.__root.geometry("360x340")
        centralizar(self.__root)
        self.__root.resizable(False, False)
        self.__root.protocol("WM_DELETE_WINDOW", self.__fechar_janela)

        if master is not None:
            self.__root.withdraw()

        cor_fundo = "#f4f6f9"
        cor_botao = "#68bced"
        cor_botao_voltar = "#777777"
        cor_texto_escuro = "#1f2937"
        cor_texto_secundario = "#6b7280"

        self.__root.configure(bg=cor_fundo)

        self.__cpf_var = tk.StringVar()
        self.__senha_var = tk.StringVar()
        self.__opcao = None

        frame_principal = tk.Frame(self.__root, bg=cor_fundo)
        frame_principal.pack(fill="both", expand=True, padx=24, pady=24)

        titulo = tk.Label(
            frame_principal,
            text="LOGIN",
            font=("Segoe UI", 20, "bold"),
            bg=cor_fundo,
            fg=cor_texto_escuro
        )
        titulo.pack(pady=(0, 4))

        subtitulo = tk.Label(
            frame_principal,
            text="Acesse o sistema",
            font=("Segoe UI", 10),
            bg=cor_fundo,
            fg=cor_texto_secundario
        )
        subtitulo.pack(pady=(0, 18))

        frame_campos = tk.Frame(frame_principal, bg=cor_fundo)
        frame_campos.pack(fill="x")

        label_cpf = tk.Label(frame_campos, text="CPF:", anchor="w", bg=cor_fundo, fg=cor_texto_escuro)
        label_cpf.pack(fill="x")
        entrada_cpf = tk.Entry(
            frame_campos,
            textvariable=self.__cpf_var,
            relief="solid",
            bd=1,
            width=30
        )
        entrada_cpf.pack(fill="x", pady=(4, 8))

        label_senha = tk.Label(frame_campos, text="Senha:", anchor="w", bg=cor_fundo, fg=cor_texto_escuro)
        label_senha.pack(fill="x")
        entrada_senha = tk.Entry(
            frame_campos,
            textvariable=self.__senha_var,
            show="*",
            relief="solid",
            bd=1,
            width=30
        )
        entrada_senha.pack(fill="x", pady=(4, 12))

        frame_botoes = tk.Frame(frame_principal, bg=cor_fundo)
        frame_botoes.pack(pady=8)

        botao_login = tk.Button(
            frame_botoes,
            text="Entrar",
            width=14,
            height=2,
            bg=cor_botao,
            fg="white",
            activebackground=cor_botao,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.__realizar_login
        )
        botao_login.pack(side="left", padx=5)

        botao_cancelar = tk.Button(
            frame_botoes,
            text="Cancelar",
            width=14,
            height=2,
            bg=cor_botao_voltar,
            fg="white",
            activebackground=cor_botao_voltar,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.__cancelar
        )
        botao_cancelar.pack(side="left", padx=5)

        rodape = tk.Label(
            frame_principal,
            text="Sistema de Gerenciamento de Cemitério",
            font=("Segoe UI", 8),
            bg=cor_fundo,
            fg="#9ca3af"
        )
        rodape.pack(pady=(16, 0))

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
