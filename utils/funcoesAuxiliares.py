import re
import tkinter as tk

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


def formatar_cpf(cpf: str):

    if cpf:

        cpf_numeros = ''.join(
            filter(str.isdigit, cpf)
        )[:11]

        if len(cpf_numeros) == 11:

            return (
                f"{cpf_numeros[:3]}."
                f"{cpf_numeros[3:6]}."
                f"{cpf_numeros[6:9]}-"
                f"{cpf_numeros[9:]}"
            )

    return cpf