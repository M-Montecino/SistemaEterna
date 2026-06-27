import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
from utils.funcoesAuxiliares import centralizar


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
        codigo = simpledialog.askinteger(
            "Cadastro",
            "Digite o código:"
        )
        if codigo is None: return None

        tumulo = simpledialog.askinteger(
            "Cadastro",
            "Digite o túmulo:"
        )
        if tumulo is None: return None

        tipo = simpledialog.askstring(
            "Cadastro",
            "Tipo de serviço (Limpeza/Reparo/Outro):"
        )
        if tipo is None: return None

        data_str = simpledialog.askstring(
            "Cadastro",
            "Digite a data (dd/mm/aaaa):"
        )
        if data_str is None: return None

        cpf = simpledialog.askstring(
            "Cadastro",
            "Digite o CPF:"
        )
        if cpf is None: return None

        data = datetime.strptime(data_str, "%d/%m/%Y")

        return {
            "codigo": codigo,
            "tumulo": tumulo,
            "tipo_servico": tipo,
            "data": data,
            "cpf_responsavel": cpf
        }

    #Auxiliar de alteração
    def alterar_manutencao(self):
        return simpledialog.askinteger(
            "Alterar",
            "Digite o código da manutenção:"
        )
    
    def pega_novos_dados_manutencao(self):
        tumulo = simpledialog.askstring(
            "Alterar",
            "Novo túmulo (vazio para manter):"
        )
        if tumulo is None: return None

        tipo = simpledialog.askstring(
            "Alterar",
            "Novo tipo (Limpeza/Reparo/Outro):"
        )
        if tipo is None: return None

        data_str = simpledialog.askstring(
            "Alterar",
            "Nova data (dd/mm/aaaa):"
        )
        if data_str is None: return None

        data = None
        cpf = simpledialog.askstring(
            "Alterar",
            "Novo CPF:"
        )
        if cpf is None: return None

        if data_str:
            data = datetime.strptime(
                data_str,
                "%d/%m/%Y"
            )

        return {
            "tumulo": int(tumulo) if tumulo else None,
            "tipo_servico": tipo if tipo else None,
            "data": data,
            "cpf_responsavel":
                cpf if cpf else None
        }

    #Auxiliar de Exclusão
    def excluir_manutencao(self):
        return simpledialog.askinteger(
            "Excluir",
            "Digite o código:"
        )
    
    #Auxiliar de Busca
    def buscar_manutencao(self):
        return simpledialog.askinteger(
            "Buscar",
            "Digite o código:"
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