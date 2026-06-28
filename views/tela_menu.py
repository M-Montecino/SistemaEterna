import tkinter as tk
from tkinter import messagebox
from utils.funcoesAuxiliares import centralizar

class TelaMenu:
    def __init__(self, master=None):
        if master is None:
            self.__root = tk.Tk()
        else:
            self.__root = tk.Toplevel(master)
            self.__root.transient(master)

        self.__root.title("Sistema Eterna")
        self.__root.geometry("400x800")
        centralizar(self.__root)
        self.__root.resizable(False, False)
        self.__root.protocol("WM_DELETE_WINDOW", self.__fechar_janela)

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
            text="MENU PRINCIPAL",
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

#Botão
        botoes = [
            ("Manutenção", 1),
            ("Túmulo", 2),
            ("Sepultamento", 3),
            ("Responsável", 4),
            ("Usuário", 5),
            ("Exumação", 6),
            ("Relatório Gerencial", 7),
            ("Logout", 8),
            ("Encerrar Sistema", 0)
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

    def __fechar_janela(self):
        self.__opcao = 0
        self.__root.quit()
        
    def mostra_relatorio_gerencial(self, dados):
        janela = tk.Toplevel(self.__root)
        janela.title("Relatório Gerencial")
        janela.geometry("520x520")
        janela.resizable(False, False)

        titulo = tk.Label(
            janela,
            text="RELATÓRIO GERENCIAL",
            font=("Segoe UI", 16, "bold")
        )
        titulo.pack(pady=15)

        texto = (
            f"Total de túmulos cadastrados: {dados['total_tumulos_cadastrados']}\n"
            f"Total de túmulos vazios: {dados['total_tumulos_vazios']}\n"
            f"Total de túmulos parcialmente ocupados: {dados['total_tumulos_parcialmente_ocupados']}\n"
            f"Total de túmulos lotados: {dados['total_tumulos_lotados']}\n\n"

            f"Capacidade total do cemitério: {dados['capacidade_total_cemiterio']}\n"
            f"Total de vagas ocupadas: {dados['total_vagas_ocupadas']}\n"
            f"Total de vagas livres: {dados['total_vagas_livres']}\n\n"

            f"Total de sepultamentos ativos: {dados['total_sepultamentos_ativos']}\n"
            f"Total de exumações realizadas: {dados['total_exumacoes_realizadas']}\n\n"

            f"Total de usuários gestores: {dados['total_usuarios_gestores']}\n"
            f"Total de usuários secretários: {dados['total_usuarios_secretarios']}"
        )

        label = tk.Label(
            janela,
            text=texto,
            font=("Segoe UI", 11),
            justify="left",
            anchor="w"
        )
        label.pack(padx=30, pady=10, anchor="w")

        tk.Button(
            janela,
            text="Fechar",
            width=20,
            command=janela.destroy
        ).pack(pady=20)

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