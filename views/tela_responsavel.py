import tkinter as tk
from tkinter import simpledialog, messagebox
from utils.funcoesAuxiliares import centralizar


class TelaResponsavel:
    def __init__(self, master=None):
        self.__root = tk.Toplevel(master)
        self.__root.title("Responsáveis")
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
            text="RESPONSÁVEL",
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
            ("Cadastrar Responsável", 1),
            ("Alterar Responsável", 2),
            ("Excluir Responsável", 3),
            ("Listar Responsáveis", 4),
            ("Buscar Responsável", 5),
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
    def pegar_dados_responsavel(self):
        janela = tk.Toplevel(self.__root)
        janela.title("Cadastro de Responsável")
        janela.geometry("450x360")

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

        tk.Label(janela, text="Data Nasc. (DD/MM/AAAA)").place(x=0, y=240)
        data_nascimento = tk.Entry(janela)
        data_nascimento.place(x=150, y=240)

        def confirmar():
            nonlocal dados

            dados = {
                "nome": nome.get(),
                "cpf": cpf.get(),
                "telefone": telefone.get(),
                "cep": cep.get(),
                "numero": int(numero.get()),
                "email": email.get(),
                "data_nascimento": data_nascimento.get()
            }

            janela.destroy()

        tk.Button(
            janela,
            text="Confirmar",
            command=confirmar
        ).place(x=170, y=300)

        janela.protocol(
            "WM_DELETE_WINDOW",
            lambda: janela.destroy()
        )

        janela.wait_window()

        return dados

    def pega_novos_dados_responsavel(self):
        janela = tk.Toplevel(self.__root)
        janela.title("Alterar Responsável")
        janela.geometry("450x360")

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

        tk.Label(janela, text="Nova Data Nasc.").place(x=0, y=200)
        data_nascimento = tk.Entry(janela)
        data_nascimento.place(x=150, y=200)

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

            dados["data_nascimento"] = (
                data_nascimento.get() if data_nascimento.get() else None
            )

            janela.destroy()

        tk.Button(
            janela,
            text="Confirmar",
            command=confirmar
        ).place(x=170, y=270)

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