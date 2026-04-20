from models.responsavel import Responsavel

# python -m testes.testes_responsavel

def testar_criacao():
    r = Responsavel(
        "Victor",
        "529.982.247-25",
        "99999-9999",
        "88000-000",
        123,
        "victor@email.com"
    )

    assert r.nome == "Victor"
    assert r.cpf == "529.982.247-25"
    assert r.telefone == "99999-9999"
    assert r.cep == "88000-000"
    assert r.numero == 123
    assert r.email == "victor@email.com"


def testar_setters_validos():
    r = Responsavel(
        "Victor",
        "529.982.247-25",
        "99999-9999",
        "88000-000",
        123,
        "victor@email.com"
    )

    r.nome = "  João  "
    r.cpf = "11597679984"
    r.telefone = "88888-8888"
    r.cep = "89000-000"
    r.numero = 456
    r.email = "joao@email.com"

    assert r.nome == "João"
    assert r.cpf == "11597679984"
    assert r.telefone == "88888-8888"
    assert r.cep == "89000-000"
    assert r.numero == 456
    assert r.email == "joao@email.com"


def testar_erros():
    r = Responsavel(
        "Victor",
        "529.982.247-25",
        "99999-9999",
        "88000-000",
        123,
        "victor@email.com"
    )

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
        r.cpf = "12345678900"
        assert False, "cpf deveria falhar inválido"
    except ValueError:
        pass

    try:
        r.cpf = 123
        assert False, "cpf deveria falhar com tipo inválido"
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


if __name__ == "__main__":
    rodar_testes()