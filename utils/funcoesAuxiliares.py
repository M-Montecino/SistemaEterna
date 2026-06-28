import re
import tkinter as tk


def centralizar(janela):
    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (janela.winfo_width() // 2)
    y = (janela.winfo_screenheight() // 2) - (janela.winfo_height() // 2)
    janela.geometry(f"+{x}+{y}")


def criar_popup_modal(master, titulo, subtitulo=None, largura=420, altura=320):
    parent = None

    if master is not None:
        try:
            parent_widget = master.winfo_toplevel()
            if getattr(parent_widget, "state", "") != "withdrawn":
                parent = parent_widget
        except Exception:
            parent = None

    if parent is None:
        parent = tk._default_root

    if parent is None:
        parent = tk.Tk()

    janela = tk.Toplevel(parent)
    janela.title(titulo)
    janela.geometry(f"{largura}x{altura}")
    janela.configure(bg="#f4f6f9")
    janela.resizable(False, False)
    centralizar(janela)
    janela.lift()
    janela.update_idletasks()
    janela.focus_force()

    container = tk.Frame(janela, bg="#f4f6f9")
    container.pack(fill="both", expand=True, padx=24, pady=24)

    tk.Label(
        container,
        text=titulo,
        font=("Segoe UI", 16, "bold"),
        bg="#f4f6f9",
        fg="#1f2937"
    ).pack(anchor="w")

    if subtitulo:
        tk.Label(
            container,
            text=subtitulo,
            font=("Segoe UI", 10),
            bg="#f4f6f9",
            fg="#6b7280"
        ).pack(anchor="w", pady=(2, 12))

    return janela, container


def criar_entrada_estilizada(container, texto, show=None, width=30):
    frame = tk.Frame(container, bg="#f4f6f9")
    frame.pack(fill="x", pady=(0, 8))

    tk.Label(
        frame,
        text=texto,
        anchor="w",
        bg="#f4f6f9",
        fg="#1f2937",
        font=("Segoe UI", 10)
    ).pack(fill="x")

    entrada = tk.Entry(
        frame,
        width=width,
        relief="solid",
        bd=1,
        font=("Segoe UI", 10)
    )

    if show is not None:
        entrada.configure(show=show)

    entrada.pack(fill="x", pady=(4, 0))
    return entrada


def criar_botao_confirmacao(container, comando, texto="Confirmar"):
    botao = tk.Button(
        container,
        text=texto,
        width=16,
        height=2,
        bg="#68bced",
        fg="white",
        activebackground="#68bced",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=comando
    )
    botao.pack(pady=(12, 0), anchor="e")
    return botao


def pedir_dado(master, titulo, mensagem, tipo="texto", valor_inicial="", mostrar=None):
    janela, container = criar_popup_modal(master, titulo, subtitulo=mensagem, largura=360, altura=220)
    entrada = criar_entrada_estilizada(container, mensagem, show=mostrar)
    if valor_inicial:
        entrada.insert(0, valor_inicial)

    resultado = {"valor": None}

    def confirmar():
        valor = entrada.get().strip()
        if tipo == "inteiro":
            try:
                resultado["valor"] = int(valor) if valor else None
            except ValueError:
                resultado["valor"] = None
        else:
            resultado["valor"] = valor if valor else None
        janela.destroy()

    def fechar():
        resultado["valor"] = None
        janela.destroy()

    criar_botao_confirmacao(container, confirmar)
    janela.protocol("WM_DELETE_WINDOW", fechar)
    janela.bind("<Return>", lambda event: confirmar())
    entrada.focus_set()
    janela.wait_window()
    return resultado["valor"]

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf) #se ñ é digito = vazio

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma = 0
    for i in range(9):
        soma += int((cpf[i])) * (10 - i)
    dig1 = (soma * 10 % 11) % 10

    soma2 = 0
    for i in range(10):
        soma2 += int((cpf[i])) * (11 - i)
    dig2 = (soma2 * 10 % 11) % 10

    return cpf[-2:] == f"{dig1}{dig2}"


def validar_email(email: str) -> bool:
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None  #se for válido seguindo o padrão == true

def validar_cep(cep: str) -> bool:
    cep = re.sub(r'\D', '', cep)
    return len(cep) == 8

def validar_telefone(telefone: str) -> bool:
    telefone = re.sub(r'\D', '', telefone)
    return len(telefone) == 11

def mascara_data(event):
    texto = event.widget.get()

    texto = texto.replace("/", "")

    if len(texto) > 2:
        texto = texto[:2] + "/" + texto[2:]

    if len(texto) > 5:
        texto = texto[:5] + "/" + texto[5:]

    event.widget.delete(0, tk.END)
    event.widget.insert(0, texto[:10])


def limpar_cpf(cpf: str):
    return ''.join(filter(str.isdigit, cpf))