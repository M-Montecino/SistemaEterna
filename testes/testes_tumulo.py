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

    t.setor = "  B  "   
    t.numero = 0        
    t.tipo = TipoTumulo.Cripta
    t.capacidade = 0    
    t.lotado = True

    assert t.setor == "B"
    assert t.numero == 0
    assert t.tipo == TipoTumulo.Cripta
    assert t.capacidade == 0
    assert t.lotado is True


def testar_erros():
    t = Tumulo(1, "A", 10, TipoTumulo.Cova, 3)

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

    t_para_alterar = [t for t in registros if t.codigo == 3 ][0]
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

    tumulos: list[Tumulo] = []

    def verificar_codigo_unico(codigo: int) -> bool:
        return all(t.codigo != codigo for t in tumulos)

    def listar_tumulos(tumulos):
        if not tumulos:
            print(">> Nenhum túmulo cadastrado.")
        else:
            for t in tumulos:
                print(f'ID: {t.codigo} | Setor: {t.setor} | Tipo: {t.tipo.name} | Capacidade: {t.capacidade} | Lotado: {"não" if not t.lotado else "sim"}')

    def criar_tumulo():
        print("\n=== Criar Túmulo ===")
        try:
            codigo = int(input("Código: "))
            if not verificar_codigo_unico(codigo):
                print("Código já cadastrado.")
                return

            setor = input("Setor: ")

            numero = int(input("Número: "))

            tipo_input = input("Tipo (1-Cova, 2-Cripta, 3-Gaveteiro): ")

            tipo = TipoTumulo(int(tipo_input))

            capacidade = int(input("Capacidade: "))

            novo_tumulo = Tumulo(codigo, setor, numero, tipo, capacidade)

            tumulos.append(novo_tumulo)
            print("Túmulo criado com sucesso!")
        except Exception as e:
            print(f"Erro ao criar túmulo: {e}")

    def editar_tumulo():
        print("\n=== Editar Túmulo ===")
        try:
            codigo = int(input("Digite o código do túmulo a editar: "))

            tumulo_para_editar = [t for t in tumulos if t.codigo == codigo][0]

            setor_input = input(f"Setor ({tumulo_para_editar.setor}): ")
            setor = setor_input.strip() if setor_input.strip() else tumulo_para_editar.setor

            numero_input = input(f"Número ({tumulo_para_editar.numero}): ")
            numero = int(numero_input) if numero_input else tumulo_para_editar.numero

            tipo_input = input(f"Tipo ({tumulo_para_editar.tipo.name}) (1-Cova, 2-Cripta, 3-Gaveteiro): ")
            tipo = TipoTumulo(int(tipo_input)) if tipo_input else tumulo_para_editar.tipo

            capacidade_input = input(f"Capacidade ({tumulo_para_editar.capacidade}): ")
            capacidade = int(capacidade_input) if capacidade_input else tumulo_para_editar.capacidade

            tumulo_para_editar.setor = setor
            tumulo_para_editar.numero = numero
            tumulo_para_editar.tipo = tipo
            tumulo_para_editar.capacidade = capacidade
    
            print("Túmulo editado com sucesso!")
        except Exception as e:
            print(f"Erro ao editar túmulo: {e}")

    def excluir_tumulo():
        print("\n=== Excluir Túmulo ===")
        global tumulos
        try:
            codigo = int(input("Digite o código do túmulo a excluir: "))
            if verificar_codigo_unico(codigo):
                print("Túmulo não encontrado.")
                return

            confirmacao = input("Tem certeza que deseja excluir? (s/n): ")

            if confirmacao.lower() != 's':
                print("Exclusão cancelada.")
                return
            tumulos = [t for t in tumulos if t.codigo != codigo]
            print("Túmulo excluído com sucesso!")
        except Exception as e:
            print(f"Erro ao excluir túmulo: {e}")

    while True:
    
        print("=== Tela Inicial Tumulos ===\n \n")

        listar_tumulos(tumulos)

        print("\nOpções: [1] Criar | [2] Editar | [3] Excluir | [4] Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            criar_tumulo()
        elif opcao == "2":
            editar_tumulo()
        elif opcao == "3":
            excluir_tumulo()
        elif opcao == "4":
            exit(0)
