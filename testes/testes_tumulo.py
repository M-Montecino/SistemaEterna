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