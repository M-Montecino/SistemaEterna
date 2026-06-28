import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from utils.funcoesAuxiliares import (
    centralizar,
    criar_botao_confirmacao,
    criar_entrada_estilizada,
    criar_popup_modal,
    mascara_data,
    pedir_dado,
)


class TelaManutencao:
    def __init__(self, master=None):
        self.__root = tk.Toplevel(master)
        self.__root.title("Manutenção")
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
            text="MANUTENÇÃO",
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
            ("Cadastrar Manutenção", 1),
            ("Alterar Manutenção", 2),
            ("Excluir Manutenção", 3),
            ("Listar Manutenções", 4),
            ("Buscar Manutenção", 5),
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

    #Auxiliar de Cadastro
    def pega_dados_manutencao(self):
        janela, container = criar_popup_modal(
            self.__root,
            "Cadastro de Manutenção",
            "Informe os dados da manutenção",
            largura=460,
            altura=430
        )

        codigo = criar_entrada_estilizada(container, "Código")
        tumulo = criar_entrada_estilizada(container, "Túmulo")
        tipo = criar_entrada_estilizada(container, "Tipo de serviço (Limpeza/Reparo/Outro)")
        data_str = criar_entrada_estilizada(container, "Data (DD/MM/AAAA)")
        data_str.bind("<KeyRelease>", mascara_data)
        cpf = criar_entrada_estilizada(container, "CPF do responsável")

        resultado = None

        def confirmar():
            nonlocal resultado
            try:
                data = datetime.strptime(data_str.get().strip(), "%d/%m/%Y") if data_str.get().strip() else None
            except ValueError:
                data = None

            resultado = {
                "codigo": int(codigo.get().strip()) if codigo.get().strip() else None,
                "tumulo": int(tumulo.get().strip()) if tumulo.get().strip() else None,
                "tipo_servico": tipo.get().strip() or None,
                "data": data,
                "cpf_responsavel": cpf.get().strip() or None,
            }
            janela.destroy()

        criar_botao_confirmacao(container, confirmar)
        janela.protocol("WM_DELETE_WINDOW", lambda: janela.destroy())
        janela.bind("<Return>", lambda event: confirmar())
        janela.wait_window()

        return resultado

    #Auxiliar de alteração
    def alterar_manutencao(self):
        return pedir_dado(
            self.__root,
            "Alterar Manutenção",
            "Digite o código da manutenção:",
            tipo="inteiro"
        )
    
    def pega_novos_dados_manutencao(self):
        janela, container = criar_popup_modal(
            self.__root,
            "Alterar Manutenção",
            "Atualize os dados da manutenção",
            largura=460,
            altura=430
        )

        tumulo = criar_entrada_estilizada(container, "Novo túmulo")
        tipo = criar_entrada_estilizada(container, "Novo tipo (Limpeza/Reparo/Outro)")
        data_str = criar_entrada_estilizada(container, "Nova data (DD/MM/AAAA)")
        data_str.bind("<KeyRelease>", mascara_data)
        cpf = criar_entrada_estilizada(container, "Novo CPF")

        resultado = None

        def confirmar():
            nonlocal resultado
            try:
                data = datetime.strptime(data_str.get().strip(), "%d/%m/%Y") if data_str.get().strip() else None
            except ValueError:
                data = None

            resultado = {
                "tumulo": int(tumulo.get().strip()) if tumulo.get().strip() else None,
                "tipo_servico": tipo.get().strip() or None,
                "data": data,
                "cpf_responsavel": cpf.get().strip() or None,
            }
            janela.destroy()

        criar_botao_confirmacao(container, confirmar)
        janela.protocol("WM_DELETE_WINDOW", lambda: janela.destroy())
        janela.bind("<Return>", lambda event: confirmar())
        janela.wait_window()

        return resultado

    #Auxiliar de Exclusão
    def excluir_manutencao(self):
        return pedir_dado(
            self.__root,
            "Excluir Manutenção",
            "Digite o código:",
            tipo="inteiro"
        )
    
    #Auxiliar de Busca
    def buscar_manutencao(self):
        return pedir_dado(
            self.__root,
            "Buscar Manutenção",
            "Digite o código:",
            tipo="inteiro"
        )

    #Funções de navegção
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
        messagebox.showinfo("Mensagem", mensagem) 