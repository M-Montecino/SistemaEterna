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
        janela, container = criar_popup_modal(
            self.__root,
            "Cadastro de Responsável",
            "Preencha os dados abaixo",
            largura=460,
            altura=600
        )

        nome = criar_entrada_estilizada(container, "Nome")
        cpf = criar_entrada_estilizada(container, "CPF")
        telefone = criar_entrada_estilizada(container, "Telefone")
        cep = criar_entrada_estilizada(container, "CEP")
        numero = criar_entrada_estilizada(container, "Número")
        email = criar_entrada_estilizada(container, "Email")
        data_nascimento = criar_entrada_estilizada(container, "Data de nascimento (DD/MM/AAAA)")
        data_nascimento.bind("<KeyRelease>", mascara_data)

        dados = None

        def confirmar():
            nonlocal dados

            valor_numero = numero.get().strip()
            try:
                numero_convertido = int(valor_numero) if valor_numero else None
            except ValueError:
                numero_convertido = None

            dados = {
                "nome": nome.get().strip() or None,
                "cpf": cpf.get().strip() or None,
                "telefone": telefone.get().strip() or None,
                "cep": cep.get().strip() or None,
                "numero": numero_convertido,
                "email": email.get().strip() or None,
                "data_nascimento": data_nascimento.get().strip() or None,
            }
            janela.destroy()

        criar_botao_confirmacao(container, confirmar)
        janela.protocol("WM_DELETE_WINDOW", lambda: janela.destroy())
        janela.bind("<Return>", lambda event: confirmar())
        janela.wait_window()

        return dados

    def pega_novos_dados_responsavel(self):
        janela, container = criar_popup_modal(
            self.__root,
            "Alterar Responsável",
            "Atualize apenas os campos desejados",
            largura=460,
            altura=500,
        )

        dados = {}

        nome = criar_entrada_estilizada(container, "Novo nome")
        telefone = criar_entrada_estilizada(container, "Novo telefone")
        cep = criar_entrada_estilizada(container, "Novo CEP")
        numero = criar_entrada_estilizada(container, "Novo número")
        email = criar_entrada_estilizada(container, "Novo email")
        data_nascimento = criar_entrada_estilizada(container, "Nova data de nascimento")
        data_nascimento.bind("<KeyRelease>", mascara_data)

        def confirmar():
            valor_numero = numero.get().strip()
            try:
                numero_convertido = int(valor_numero) if valor_numero else None
            except ValueError:
                numero_convertido = None

            dados["nome"] = nome.get().strip() or None
            dados["telefone"] = telefone.get().strip() or None
            dados["cep"] = cep.get().strip() or None
            dados["numero"] = numero_convertido
            dados["email"] = email.get().strip() or None
            dados["data_nascimento"] = data_nascimento.get().strip() or None
            janela.destroy()

        criar_botao_confirmacao(container, confirmar)
        janela.protocol("WM_DELETE_WINDOW", lambda: janela.destroy())
        janela.bind("<Return>", lambda event: confirmar())
        janela.wait_window()

        return dados

    def alterar_responsavel(self):
        return pedir_dado(
            self.__root,
            "Alterar Responsável",
            "CPF do responsável:",
            tipo="texto"
        )

    def excluir_responsavel(self):
        return pedir_dado(
            self.__root,
            "Excluir Responsável",
            "CPF do responsável:",
            tipo="texto"
        )

    def buscar_responsavel(self):
        return pedir_dado(
            self.__root,
            "Buscar Responsável",
            "CPF do responsável:",
            tipo="texto"
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