import tkinter as tk
from tkinter import messagebox, simpledialog

class TelaUsuario:
    def __init__(self, master=None):
        self.__root = tk.Toplevel(master)
        self.__root.title("Usuários")
        self.__root.geometry("400x600")
        self.__root.resizable(False, False)
        self.__root.protocol("WM_DELETE_WINDOW", self.__fechar_janela)
        self.__root.transient(master)
        self.__root.withdraw()

        self.__opcao = None

        # Cores
        COR_FUNDO = "#f4f6f9"
        COR_BOTAO = "#68bced"
        COR_BOTAO_VOLTAR = "#777777"
        COR_TEXTO = "white"
        
        self.__root.configure(bg=COR_FUNDO)

#Título
        titulo = tk.Label(
            self.__root,
            text="USUÁRIO",
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
            ("Cadastrar Usuário", 1),
            ("Alterar Usuário", 2),
            ("Excluir Usuário", 3),
            ("Listar Usuários", 4),
            ("Buscar Usuário", 5),
            ("Voltar", 0)
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

    def pega_dados_cadastro(self):
        nome = simpledialog.askstring("Cadastro", "Nome:", parent=self.__root)
        if nome is None:
            return None

        cargo = simpledialog.askstring(
            "Cadastro",
            "Cargo (1- Gestor, 2- Secretário):",
            parent=self.__root
        )
        if cargo is None:
            return None

        email = simpledialog.askstring("Cadastro", "Email:", parent=self.__root)
        if email is None:
            return None

        cpf = simpledialog.askstring("Cadastro", "CPF:", parent=self.__root)
        if cpf is None:
            return None

        senha = simpledialog.askstring(
            "Cadastro",
            "Senha:",
            parent=self.__root,
            show="*"
        )
        if senha is None:
            return None

        return {
            "nome": nome,
            "cargo": cargo,
            "email": email,
            "cpf": cpf,
            "senha": senha
        }

    def pega_dados_busca(self):
        cpf = simpledialog.askstring("Buscar", "CPF do usuário:", parent=self.__root)
        return cpf

    def pega_dados_exclusao(self):
        cpf = simpledialog.askstring("Excluir", "CPF do usuário:", parent=self.__root)
        return cpf

    def pega_dados_alteracao(self):
        cpf = simpledialog.askstring("Alterar", "CPF do usuário:", parent=self.__root)
        if cpf is None:
            return None

        novo_nome = simpledialog.askstring("Alterar", "Novo nome:", parent=self.__root)
        novo_email = simpledialog.askstring("Alterar", "Novo email:", parent=self.__root)
        novo_cargo = simpledialog.askstring(
            "Alterar",
            "Novo cargo (1- Gestor, 2- Secretário):",
            parent=self.__root
        )
        nova_senha = simpledialog.askstring(
            "Alterar",
            "Nova senha (vazio para manter):",
            parent=self.__root,
            show="*"
        )

        return {
            "cpf": cpf,
            "nome": novo_nome,
            "email": novo_email,
            "cargo": novo_cargo,
            "senha": nova_senha
        }

    def mostra_mensagem(self, mensagem):
        messagebox.showinfo("Mensagem", mensagem, parent=self.__root)

    def __fechar_janela(self):
        self.__opcao = 0
        self.__root.quit()
