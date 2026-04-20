from models.tumulo import Tumulo, TipoTumulo
# python -m testes.testes_tumulo

def testar_criacao():
    t = Tumulo(1, "A", 10, TipoTumulo.Cova, 3)

    assert t.codigo == 1
    assert t.setor == "A"
    assert t.numero == 10
    assert t.tipo == TipoTumulo.Cova
    assert t.capacidade == 3
    assert t.lotado is False


def testar_setters_validos():
    t = Tumulo(1, "A", 10, TipoTumulo.Cova, 3)

    t.codigo = 2
    t.setor = "  B  "   
    t.numero = 0        
    t.tipo = TipoTumulo.Cripta
    t.capacidade = 0    
    t.lotado = True

    assert t.codigo == 2
    assert t.setor == "B"
    assert t.numero == 0
    assert t.tipo == TipoTumulo.Cripta
    assert t.capacidade == 0
    assert t.lotado is True


def testar_erros():
    t = Tumulo(1, "A", 10, TipoTumulo.Cova, 3)

    try:
        t.codigo = 0
        assert False, "codigo deveria falhar com 0"
    except ValueError:
        pass

    try:
        t.codigo = "abc"
        assert False, "codigo deveria falhar com string"
    except ValueError:
        pass

    try:
        t.setor = 123
        assert False, "setor deveria falhar"
    except ValueError:
        pass

    try:
        t.numero = -1
        assert False, "numero deveria falhar"
    except ValueError:
        pass

    try:
        t.tipo = "Cova"
        assert False, "tipo deveria falhar"
    except ValueError:
        pass

    try:
        t.capacidade = -1
        assert False, "capacidade deveria falhar"
    except ValueError:
        pass

    try:
        t.capacidade = "muito"
        assert False, "capacidade deveria falhar com string"
    except ValueError:
        pass

    try:
        t.lotado = "sim"
        assert False, "lotado deveria falhar"
    except ValueError:
        pass

def testar_fluxo_crud():
    registros = []

    t1 = Tumulo(1, "A", 10, TipoTumulo.Cova, 3)
    t2 = Tumulo(2, "B", 20, TipoTumulo.Cripta, 5)
    t3 = Tumulo(3, "C", 30, TipoTumulo.Gaveteiro, 2)
    registros.extend([t1, t2, t3])
    
    assert len(registros) == 3

    print("\nListagem Inicial:")
    for t in registros:
        print(f"ID: {t.codigo} | Setor: {t.setor} | Tipo: {t.tipo.name} | Capacidade: {t.capacidade} | Lotado: {t.lotado}")

    codigo_para_excluir = 2
    registros = [t for t in registros if t.codigo != codigo_para_excluir]
    
    assert len(registros) == 2
    assert all(t.codigo != 2 for t in registros)

    print("\nListagem após exclusão:")
    for t in registros:
        print(f"ID: {t.codigo} | Setor: {t.setor} | Tipo: {t.tipo.name} | Capacidade: {t.capacidade} | Lotado: {t.lotado}")

    t_para_alterar = next(t for t in registros if t.codigo == 3)
    t_para_alterar.setor = "Z"
    t_para_alterar.numero = 99
    t_para_alterar.tipo = TipoTumulo.Cripta

    assert t_para_alterar.setor == "Z"
    assert t_para_alterar.numero == 99
    assert t_para_alterar.tipo == TipoTumulo.Cripta

    print("\nListagem após alteração do ID 3:")
    for t in registros:
        print(f"ID: {t.codigo} | Setor: {t.setor} | Num: {t.numero} | Tipo: {t.tipo.name} | Capacidade: {t.capacidade} | Lotado: {t.lotado}")

    t4 = Tumulo(4, "D", 40, TipoTumulo.Cova, 1)
    registros.append(t4)

    assert len(registros) == 3
    assert registros[-1].codigo == 4

    print("\nListagem Final:")
    for t in registros:
        print(f"ID: {t.codigo} | Setor: {t.setor} | Tipo: {t.tipo.name} | Capacidade: {t.capacidade} | Lotado: {t.lotado}")

def rodar_testes():
    print("Rodando testes...")

    testar_criacao()
    print("criação OK")

    testar_setters_validos()
    print("setters OK")

    testar_erros()
    print("erros OK")

    testar_fluxo_crud()
    print("fluxo CRUD OK")


if __name__ == "__main__":
    rodar_testes()