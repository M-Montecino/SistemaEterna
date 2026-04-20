from models.responsavel import Responsavel
import re
# python -m testes.testes_responsavel

def testar_criacao():
    r = Responsavel(
        "Victor",
        "529.982.247-25",
        "99999999999",
        "88000-000",
        123,
        "victor@email.com"
    )

    assert r.nome == "Victor"
    assert r.cpf == "529.982.247-25"
    assert r.telefone == "99 99999-9999"
    assert r.cep == "88000-000"
    assert r.numero == 123
    assert r.email == "victor@email.com"


def testar_setters_validos():
    r = Responsavel(
        "Victor",
        "529.982.247-25",
        "99999999999",
        "88000-000",
        123,
        "victor@email.com"
    )

    r.nome = "  João  "
    r.telefone = "88888888888"
    r.cep = "89000-000"
    r.numero = 456
    r.email = "joao@email.com"

    assert r.nome == "João"
    assert r.telefone == "88 88888-8888"
    assert r.cep == "89000-000"
    assert r.numero == 456
    assert r.email == "joao@email.com"


def testar_erros():
    r = Responsavel(
        "Victor",
        "529.982.247-25",
        "99999999999",
        "88000-000",
        123,
        "victor@email.com"
    )


def testar_fluxo_crud_responsavel():
    registros = []

    r1 = Responsavel("Ana", "52998224725", "11111111111", "88000-000", 10, "ana@email.com")
    r2 = Responsavel("Bruno", "11144477735", "22222222222", "88000-001", 20, "bruno@email.com")
    r3 = Responsavel("Carlos", "93541134780", "33333333333", "88000-002", 30, "carlos@email.com")

    registros.extend([r1, r2, r3])

    assert len(registros) == 3

    print("\nListagem Inicial:")
    for r in registros:
        print(f"Nome: {r.nome} | CPF: {r.cpf} | Telefone: {r.telefone} | CEP: {r.cep} | Email: {r.email} | Nº: {r.numero}")

    cpf_para_excluir = "11144477735"
    registros = [r for r in registros if re.sub(r'\D', '', r.cpf) != cpf_para_excluir]

    assert len(registros) == 2
    assert all(r.cpf != cpf_para_excluir for r in registros)

    print("\nListagem após exclusão:")
    for r in registros:
        print(f"Nome: {r.nome} | CPF: {r.cpf} | Telefone: {r.telefone} | CEP: {r.cep} | Email: {r.email} | Nº: {r.numero}")

    r_para_alterar = next(r for r in registros if re.sub(r'\D', '', r.cpf) == "93541134780")

    r_para_alterar.nome = "Carlos Silva"
    r_para_alterar.numero = 99
    r_para_alterar.email = "carlos.silva@email.com"

    assert r_para_alterar.nome == "Carlos Silva"
    assert r_para_alterar.numero == 99
    assert r_para_alterar.email == "carlos.silva@email.com"

    print("\nListagem após alteração:")
    for r in registros:
        print(f"Nome: {r.nome} | CPF: {r.cpf} | Telefone: {r.telefone} | CEP: {r.cep} | Email: {r.email} | Nº: {r.numero}")

    r4 = Responsavel("Daniel", "28625587887", "44444444444", "88000-003", 40, "daniel@email.com")
    registros.append(r4)

    assert len(registros) == 3
    assert re.sub(r'\D', '', registros[-1].cpf) == "28625587887"

    print("\nListagem Final:")
    for r in registros:
        print(f"Nome: {r.nome} | CPF: {r.cpf} | Telefone: {r.telefone} | CEP: {r.cep} | Email: {r.email} | Nº: {r.numero}")

    try:
        r.nome = ""
        assert False, "nome deveria falhar vazio"
    except ValueError:
        pass

    try:
        r.nome = 123
        assert False, "nome deveria falhar com tipo inválido"
    except ValueError:
        pass

    try:
        r.telefone = 999999
        assert False, "telefone deveria falhar"
    except ValueError:
        pass

    try:
        r.cep = 12345678
        assert False, "cep deveria falhar"
    except ValueError:
        pass

    try:
        r.numero = "casa"
        assert False, "numero deveria falhar"
    except ValueError:
        pass

    try:
        r.email = "email_invalido"
        assert False, "email deveria falhar"
    except ValueError:
        pass

    try:
        r.email = 123
        assert False, "email deveria falhar com tipo inválido"
    except ValueError:
        pass


def rodar_testes():
    print("Rodando testes...")

    testar_criacao()
    print("criação OK")

    testar_setters_validos()
    print("setters OK")

    testar_erros()
    print("erros OK")

    testar_fluxo_crud_responsavel()
    print("fluxo CRUD OK")


if __name__ == "__main__":
    rodar_testes()


import re
from models.responsavel import Responsavel

responsaveis: list[Responsavel] = []

def limpar_cpf(cpf: str) -> str:
    return re.sub(r'\D', '', cpf)

def verificar_cpf_unico(cpf: str) -> bool:
    cpf = limpar_cpf(cpf)
    return all(limpar_cpf(r.cpf) != cpf for r in responsaveis)

def listar_responsaveis(lista):
    if not lista:
        print(">> Nenhum responsável cadastrado.")
    else:
        for r in lista:
            print(f'Nome: {r.nome} | CPF: {r.cpf} | Telefone: {r.telefone} | CEP: {r.cep} | Nº: {r.numero} | Email: {r.email}')

def criar_responsavel():
    print("\n=== Criar Responsável ===")
    try:
        nome = input("Nome: ")
        cpf = input("CPF: ")

        if not verificar_cpf_unico(cpf):
            print("CPF já cadastrado.")
            return

        telefone = input("Telefone: ")
        cep = input("CEP: ")
        numero = int(input("Número: "))
        email = input("Email: ")

        novo = Responsavel(nome, cpf, telefone, cep, numero, email)
        responsaveis.append(novo)

        print("Responsável criado com sucesso!")

    except Exception as e:
        print(f"Erro ao criar responsável: {e}")

def editar_responsavel():
    print("\n=== Editar Responsável ===")
    try:
        cpf = limpar_cpf(input("Digite o CPF do responsável: "))

        lista = [r for r in responsaveis if limpar_cpf(r.cpf) == cpf]

        if not lista:
            print("Responsável não encontrado.")
            return

        responsavel = lista[0]

        nome_input = input(f"Nome ({responsavel.nome}): ")
        nome = nome_input.strip() if nome_input.strip() else responsavel.nome

        telefone_input = input(f"Telefone ({responsavel.telefone}): ")
        telefone = telefone_input if telefone_input else responsavel.telefone

        cep_input = input(f"CEP ({responsavel.cep}): ")
        cep = cep_input if cep_input else responsavel.cep

        numero_input = input(f"Número ({responsavel.numero}): ")
        numero = int(numero_input) if numero_input else responsavel.numero

        email_input = input(f"Email ({responsavel.email}): ")
        email = email_input if email_input else responsavel.email

        responsavel.nome = nome
        responsavel.telefone = telefone
        responsavel.cep = cep
        responsavel.numero = numero
        responsavel.email = email

        print("Responsável editado com sucesso!")

    except Exception as e:
        print(f"Erro ao editar responsável: {e}")

def excluir_responsavel():
    print("\n=== Excluir Responsável ===")
    global responsaveis
    try:
        cpf = limpar_cpf(input("Digite o CPF do responsável: "))

        if verificar_cpf_unico(cpf):
            print("Responsável não encontrado.")
            return

        confirmacao = input("Tem certeza que deseja excluir? (s/n): ")

        if confirmacao.lower() != 's':
            print("Exclusão cancelada.")
            return

        responsaveis = [
            r for r in responsaveis
            if limpar_cpf(r.cpf) != cpf
        ]

        print("Responsável excluído com sucesso!")

    except Exception as e:
        print(f"Erro ao excluir responsável: {e}")


while True:
    print("\n=== Tela Inicial Responsáveis ===\n")

    listar_responsaveis(responsaveis)

    print("\nOpções: [1] Criar | [2] Editar | [3] Excluir | [4] Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        criar_responsavel()
    elif opcao == "2":
        editar_responsavel()
    elif opcao == "3":
        excluir_responsavel()
    elif opcao == "4":
        exit(0)