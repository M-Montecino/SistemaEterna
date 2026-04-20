#este arquivo será excluido posteriormente
import sys
sys.path.append('.')

from models.manutencao import Manutencao, TipoServico
from datetime import datetime
# python -m testes.testes_manutencao

def testar_criacao():
    data = datetime.now()
    m = Manutencao(1, "T1", TipoServico.Limpeza, data, "12345678900")

    assert m.codigo == 1
    assert m.tumulo == "T1"
    assert m.tipo_servico == TipoServico.Limpeza
    assert m.data == data
    assert m.cpf_responsavel == "12345678900"


def testar_setters_validos():
    data1 = datetime.now()
    data2 = datetime(2025, 1, 1)

    m = Manutencao(1, "T1", TipoServico.Limpeza, data1, "123")

    m.tumulo = "T2"
    m.tipo_servico = TipoServico.Reparo
    m.data = data2
    m.cpf_responsavel = "99999999999"

    assert m.tumulo == "T2"
    assert m.tipo_servico == TipoServico.Reparo
    assert m.data == data2
    assert m.cpf_responsavel == "99999999999"


def testar_erros():
    data = datetime.now()
    m = Manutencao(1, "T1", TipoServico.Limpeza, data, "123")

    try:
        m.tipo_servico = "Limpeza"
        assert False, "tipo_servico deveria falhar com string"
    except ValueError:
        pass

    try:
        m.data = "01/01/2025"
        assert False, "data deveria falhar com string"
    except ValueError:
        pass

    try:
        m.cpf_responsavel = 123456789
        assert False, "cpf deveria falhar com inteiro"
    except ValueError:
        pass


def testar_fluxo_crud():
    registros = []

    m1 = Manutencao(1, "T1", TipoServico.Limpeza, datetime.now(), "111")
    m2 = Manutencao(2, "T2", TipoServico.Reparo, datetime.now(), "222")
    m3 = Manutencao(3, "T3", TipoServico.Outro, datetime.now(), "333")

    registros.extend([m1, m2, m3])

    assert len(registros) == 3

    print("\nListagem Inicial:")
    for m in registros:
        print(f"ID: {m.codigo} | Tumulo: {m.tumulo} | Tipo: {m.tipo_servico.name} | CPF: {m.cpf_responsavel}")

    # deletar
    codigo_para_excluir = 2
    registros = [m for m in registros if m.codigo != codigo_para_excluir]

    assert len(registros) == 2
    assert all(m.codigo != 2 for m in registros)

    print("\nListagem após exclusão:")
    for m in registros:
        print(f"ID: {m.codigo} | Tumulo: {m.tumulo} | Tipo: {m.tipo_servico.name} | CPF: {m.cpf_responsavel}")

    # alterar
    m_para_alterar = next(m for m in registros if m.codigo == 3)
    m_para_alterar.tumulo = "T99"
    m_para_alterar.tipo_servico = TipoServico.Limpeza

    assert m_para_alterar.tumulo == "T99"
    assert m_para_alterar.tipo_servico == TipoServico.Limpeza

    print("\nListagem após alteração do ID 3:")
    for m in registros:
        print(f"ID: {m.codigo} | Tumulo: {m.tumulo} | Tipo: {m.tipo_servico.name} | CPF: {m.cpf_responsavel}")

    # criar
    m4 = Manutencao(4, "T4", TipoServico.Reparo, datetime.now(), "444")
    registros.append(m4)

    assert len(registros) == 3
    assert registros[-1].codigo == 4

    print("\nListagem Final:")
    for m in registros:
        print(f"ID: {m.codigo} | Tumulo: {m.tumulo} | Tipo: {m.tipo_servico.name} | CPF: {m.cpf_responsavel}")


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