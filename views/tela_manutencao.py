import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class TelaManutencao:
    def __init__(self, master=None):
        self.__root = tk.Toplevel(master)
        self.__root.title("Manutenção")
        self.__root.geometry("320x420")
        self.__root.resizable(False, False)
        self.__root.protocol("WM_DELETE_WINDOW", self.__fechar_janela)
        self.__root.transient(master)
        self.__root.withdraw()

        self.__opcao = None

        titulo = tk.Label(
            self.__root,
            text="MANUTENÇÃO",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        botoes = [
            ("Cadastrar Manutenção", 1),
            ("Alterar Manutenção", 2),
            ("Excluir Manutenção", 3),
            ("Listar Manutenções", 4),
            ("Buscar Manutenção", 5),
            ("Voltar ao Menu", 0)
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

    #Auxiliar de Cadastro
    def pega_dados_manutencao(self):
        codigo = int(
            simpledialog.askstring(
                "Cadastro",
                "Digite o código:"
            )
        )

        tumulo = int(simpledialog.askstring(
            "Cadastro",
            "Digite o túmulo:"
        )
        )

        tipo = simpledialog.askstring(
            "Cadastro",
            "Tipo de serviço (Limpeza/Reparo/Outro):"
        )

        data_str = simpledialog.askstring(
            "Cadastro",
            "Digite a data (dd/mm/aaaa):"
        )

        cpf = simpledialog.askstring(
            "Cadastro",
            "Digite o CPF:"
        )

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
        return int(
            simpledialog.askstring(
                "Alterar",
                "Digite o código da manutenção:"
            )
        )
    
    def pega_novos_dados_manutencao(self):
        tumulo = simpledialog.askstring(
            "Alterar",
            "Novo túmulo (vazio para manter):"
        )
        tipo = simpledialog.askstring(
            "Alterar",
            "Novo tipo (Limpeza/Reparo/Outro):"
        )
        data_str = simpledialog.askstring(
            "Alterar",
            "Nova data (dd/mm/aaaa):"
        )
        data = None
        cpf = simpledialog.askstring(
            "Alterar",
            "Novo CPF:"
        )

        if data_str:
            data = datetime.strptime(
                data_str,
                "%d/%m/%Y"
            )

        return {
            "tumulo": tumulo if tumulo else None,
            "tipo_servico": tipo if tipo else None,
            "data": data,
            "cpf_responsavel":
                cpf if cpf else None
        }

    #Auxiliar de Exclusão
    def excluir_manutencao(self):
        return int(
            simpledialog.askstring(
                "Excluir",
                "Digite o código:"
            )
        )
    
    #Auxiliar de Busca
    def buscar_manutencao(self):
        return int(
            simpledialog.askstring(
                "Buscar",
                "Digite o código:"
            )
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