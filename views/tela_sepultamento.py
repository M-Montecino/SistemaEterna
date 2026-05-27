import tkinter as tk
from tkinter import ttk
from utils.funcoesAuxiliares import mascara_data
from tkinter import (
    messagebox,
    simpledialog
)
from datetime import datetime


class TelaSepultamento:

    def __init__(
        self,
        master=None
    ):
        self.__root = tk.Toplevel(master)
        self.__root.title("Sepultamento")
        self.__root.geometry("350x450")
        self.__root.resizable(
            False,
            False)
        self.__root.protocol(
            "WM_DELETE_WINDOW",
            self.__fechar_janela
        )
        self.__root.transient(master)
        self.__root.withdraw()
        self.__opcao = None
        titulo = tk.Label(
            self.__root,
            text="SEPULTAMENTO",
            font=("Arial", 16, "bold")
        )

        titulo.pack(pady=10)

        botoes = [
            ("Cadastrar Sepultamento", 1),
            ("Alterar Sepultamento", 2),
            ("Excluir Sepultamento", 3),
            ("Listar Sepultamentos", 4),
            ("Buscar Sepultamento", 5),
            ("Voltar ao Menu", 0)
        ]

        for texto, valor in botoes:
            botao = tk.Button(
                self.__root,
                text=texto,
                width=25,
                height=2,
                command=lambda v=valor:
                    self.__selecionar_opcao(v)
            )
            botao.pack(pady=5)

    def pega_dados_sepultamento(self):
        janela_cadastro = tk.Toplevel(self.__root)
        janela_cadastro.title('Cadastro')
        janela_cadastro.geometry("500x550")

        dados = None

        tk.Label(janela_cadastro, text='CPF').place(x=0, y=0)
        cpf_falecido = tk.Entry(janela_cadastro)
        cpf_falecido.place(x=190, y=0)

        tk.Label(janela_cadastro, text='Nome').place(x=0, y=30)
        nome_falecido = tk.Entry(janela_cadastro, width=30)
        nome_falecido.place(x=190, y=30)

        tk.Label(
            janela_cadastro,
            text='Data nascimento (dd/mm/aaaa)'
        ).place(x=0, y=60)
        nascimento_str = tk.Entry(janela_cadastro)
        nascimento_str.place(x=190, y=60)
        nascimento_str.bind("<KeyRelease>", mascara_data)

        tk.Label(
            janela_cadastro,
            text='Data falecimento (dd/mm/aaaa)'
        ).place(x=0, y=90)
        falecimento_str = tk.Entry(janela_cadastro)
        falecimento_str.place(x=190, y=90)
        falecimento_str.bind("<KeyRelease>", mascara_data)


        tk.Label(
            janela_cadastro,
            text='Causa morte'
        ).place(x=0, y=120)
        causa_morte = tk.Entry(janela_cadastro, width=30)
        causa_morte.place(x=190, y=120)

        tk.Label(
            janela_cadastro,
            text='Túmulo'
        ).place(x=0, y=150)
        tumulo = tk.Entry(janela_cadastro)
        tumulo.place(x=190, y=150)

        tk.Label(janela_cadastro,text='Valor pagamento').place(x=0, y=180)
        valor = tk.Entry(janela_cadastro)
        valor.place(x=190, y=180)

        tk.Label(janela_cadastro,text='Data pagamento (dd/mm/aaaa)').place(x=0, y=210)
        pagamento_str = tk.Entry(janela_cadastro)
        pagamento_str.place(x=190, y=210)
        pagamento_str.bind("<KeyRelease>", mascara_data)

        tk.Label(janela_cadastro,text='Tipo pagamento 1 - /Débito, 2 - /Crédito 3 - pix').place(x=0, y=240)
        tipo_pagamento = ttk.Combobox(
            janela_cadastro, values=[1 ,2 ,3], state = "readonly"
        )
        tipo_pagamento.place(x=260, y=240)

        tk.Label(janela_cadastro, text='Responsável 1').place(x=0, y=270)
        responsavel = tk.Entry(janela_cadastro)
        responsavel.place(x=190, y=270)

        tk.Label(janela_cadastro,text='Responsável 2').place(x=0, y=300)
        responsavel2 = tk.Entry(janela_cadastro)
        responsavel2.place(x=190, y=300)

        tk.Label(janela_cadastro,text='Início concessão (dd/mm/aaaa)').place(x=0, y=330)
        inicio_cons_str = tk.Entry(janela_cadastro)
        inicio_cons_str.place(x=190, y=330)
        inicio_cons_str.bind("<KeyRelease>", mascara_data)


        tk.Label(janela_cadastro,text='Final concessão (dd/mm/aaaa)').place(x=0, y=360)
        final_cons_str = tk.Entry(janela_cadastro)
        final_cons_str.place(x=190, y=360)
        final_cons_str.bind("<KeyRelease>", mascara_data)

        tk.Label(janela_cadastro,text='Status (1-Ativa / 2-Carência / 3-Vencida)').place(x=0, y=390)
        status = ttk.Combobox(
            janela_cadastro, values=[1 ,2 ,3], state = "readonly"
        )
        status.place(x=270, y=390)

        tk.Label(janela_cadastro,text='Data sepultamento (dd/mm/aaaa)').place(x=0, y=420)
        sepultamento_str = tk.Entry(janela_cadastro)
        sepultamento_str.place(x=190, y=420)
        sepultamento_str.bind("<KeyRelease>", mascara_data)

        tk.Label(janela_cadastro,text='Observações').place(x=0, y=450)
        observacoes = tk.Entry(janela_cadastro,width=35)
        observacoes.place(x=190, y=450)

        

        def confirmar():
            nonlocal dados

            dados = {
                "cpf_falecido": cpf_falecido.get(),
                "nome_falecido": nome_falecido.get(),

                "data_nascimento": datetime.strptime(
                    nascimento_str.get(),
                    "%d/%m/%Y"
                ),

                "data_falecimento": datetime.strptime(
                    falecimento_str.get(),
                    "%d/%m/%Y"
                ),

                "causa_morte": causa_morte.get(),

                "tumulo": tumulo.get(),

                "valor": float(valor.get()),

                "data_pagamento": datetime.strptime(
                    pagamento_str.get(),
                    "%d/%m/%Y"
                ),

                "tipo_pagamento": tipo_pagamento.get(),

                "responsavel": responsavel.get(),

                "responsavel2": responsavel2.get(),

                "data_inicio_cons": datetime.strptime(
                    inicio_cons_str.get(),
                    "%d/%m/%Y"
                ),

                "data_final_cons": datetime.strptime(
                    final_cons_str.get(),
                    "%d/%m/%Y"
                ),

                "status": int(status.get()),

                "data_sepultamento": datetime.strptime(
                    sepultamento_str.get(),
                    "%d/%m/%Y"
                ),

                "observacoes": observacoes.get()
            }

            janela_cadastro.destroy()

        botao = tk.Button(
            janela_cadastro,
            text="Confirmar",
            command=confirmar
        )

        botao.place(x=190, y=490)

        def fechar():
            janela_cadastro.destroy()

        janela_cadastro.protocol(
            "WM_DELETE_WINDOW",
            fechar
        )

        janela_cadastro.wait_window()

        return dados

    

    def pega_novos_dados_sepultamento(self):

        janela = tk.Toplevel(self.__root)
        janela.title("Alterar Sepultamento")
        janela.geometry("500x300")

        dados = {}

        tk.Label(
            janela,
            text="Novo nome"
        ).place(x=0, y=0)

        nome = tk.Entry(
            janela,
            width=30
        )

        nome.place(x=190, y=0)

        tk.Label(
            janela,
            text="Nova data nascimento (dd/mm/aaaa)"
        ).place(x=0, y=40)

        nascimento = tk.Entry(janela)

        nascimento.place(x=210, y=40)

        nascimento.bind(
            "<KeyRelease>",
            mascara_data
        )

        tk.Label(
            janela,
            text="Nova data falecimento (dd/mm/aaaa)"
        ).place(x=0, y=80)

        falecimento = tk.Entry(janela)

        falecimento.place(x=210, y=80)

        falecimento.bind(
            "<KeyRelease>",
            mascara_data
        )

        tk.Label(
            janela,
            text="Nova causa morte"
        ).place(x=0, y=120)

        causa = tk.Entry(
            janela,
            width=30
        )

        causa.place(x=190, y=120)

        def confirmar():
            dados['nome_falecido'] = (
                nome.get()
                if nome.get()
                else None
            )

            dados['data_nascimento'] = (
                datetime.strptime(
                    nascimento.get(),
                    "%d/%m/%Y"
                )
                if nascimento.get()
                else None
            )

            dados['data_falecimento'] = (
                datetime.strptime(
                    falecimento.get(),
                    "%d/%m/%Y"
                )
                if falecimento.get()
                else None
            )

            dados['causa_morte'] = (
                causa.get()
                if causa.get()
                else None
            )

            janela.destroy()

        tk.Button(
            janela,
            text="Confirmar",
            command=confirmar
        ).place(x=190, y=180)

        janela.wait_window()

        return dados

    def pega_cpf_alteracao(self):
        cpf = simpledialog.askstring("Alterar", "CPF do falecido:")
        return cpf

    def pega_cpf_exclusao(self):
        cpf =  simpledialog.askstring("Excluir", "CPF do falecido:")
        return cpf
        
    def __selecionar_opcao(
        self, valor):
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

    def mostra_mensagem(
        self,
        mensagem
    ):

        messagebox.showinfo(
            "Mensagem",
            mensagem
        )