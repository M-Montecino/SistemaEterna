from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from utils.funcoesAuxiliares import (
    centralizar,
    criar_botao_confirmacao,
    criar_entrada_estilizada,
    criar_popup_modal,
    mascara_data,
    pedir_dado,
)

class TelaUsuario:
    def __init__(self, master=None):
        self.__root = tk.Toplevel(master)
        self.__root.title("Usuários")
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
        janela, container = criar_popup_modal(
            self.__root,
            "Cadastro de Usuário",
            "Preencha os dados do novo usuário",
            largura=460,
            altura=480
        )

        nome = criar_entrada_estilizada(container, "Nome")
        cargo = criar_entrada_estilizada(container, "Cargo (1-Gestor / 2-Secretário)")
        email = criar_entrada_estilizada(container, "Email")
        cpf = criar_entrada_estilizada(container, "CPF")
        data_nascimento = criar_entrada_estilizada(container, "Data de nascimento (DD/MM/AAAA)")
        data_nascimento.bind("<KeyRelease>", mascara_data)
        senha = criar_entrada_estilizada(container, "Senha", show="*")

        resultado = None

        def confirmar():
            nonlocal resultado
            resultado = {
                "nome": nome.get().strip() or None,
                "cargo": cargo.get().strip() or None,
                "email": email.get().strip() or None,
                "cpf": cpf.get().strip() or None,
                "data_nascimento": data_nascimento.get().strip() or None,
                "senha": senha.get().strip() or None,
            }
            janela.destroy()

        criar_botao_confirmacao(container, confirmar)
        janela.protocol("WM_DELETE_WINDOW", lambda: janela.destroy())
        janela.bind("<Return>", lambda event: confirmar())
        janela.wait_window()

        return resultado

    def pega_dados_busca(self):
        return pedir_dado(
            self.__root,
            "Buscar Usuário",
            "CPF do usuário:",
            tipo="texto"
        )

    def pega_dados_exclusao(self):
        return pedir_dado(
            self.__root,
            "Excluir Usuário",
            "CPF do usuário:",
            tipo="texto"
        )

    def pega_dados_alteracao(self):
        janela, container = criar_popup_modal(
            self.__root,
            "Alterar Usuário",
            "Atualize os dados do usuário",
            largura=460,
            altura=500
        )

        cpf = criar_entrada_estilizada(container, "CPF do usuário")
        novo_nome = criar_entrada_estilizada(container, "Novo nome")
        novo_email = criar_entrada_estilizada(container, "Novo email")
        novo_cargo = criar_entrada_estilizada(container, "Novo cargo (1-Gestor / 2-Secretário)")
        nova_senha = criar_entrada_estilizada(container, "Nova senha (vazio para manter)", show="*")
        nova_data_nascimento = criar_entrada_estilizada(container, "Nova data de nascimento (DD/MM/AAAA)")
        nova_data_nascimento.bind("<KeyRelease>", mascara_data)

        resultado = None

        def confirmar():
            nonlocal resultado
            resultado = {
                "cpf": cpf.get().strip() or None,
                "nome": novo_nome.get().strip() or None,
                "email": novo_email.get().strip() or None,
                "cargo": novo_cargo.get().strip() or None,
                "senha": nova_senha.get().strip() or None,
                "data_nascimento": nova_data_nascimento.get().strip() or None,
            }
            janela.destroy()

        criar_botao_confirmacao(container, confirmar)
        janela.protocol("WM_DELETE_WINDOW", lambda: janela.destroy())
        janela.bind("<Return>", lambda event: confirmar())
        janela.wait_window()

        return resultado

    def mostra_mensagem(self, mensagem):
        messagebox.showinfo("Mensagem", mensagem, parent=self.__root)

    def __fechar_janela(self):
        self.__opcao = 0
        self.__root.quit()
