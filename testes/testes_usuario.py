from models.usuario import Usuario, Cargo, GerenciamentoUsuario


def testar_criacao_usuario():
    u = Usuario("Joao da Silva", Cargo.Gestor, "Joao@Email.com", "123.456.789-01", "1234")

    assert u.nome == "Joao da Silva"
    assert u.cargo == Cargo.Gestor
    assert u.email == "joao@email.com"
    assert u.cpf == "12345678901"
    assert u.senha != "1234"
    assert "$" in u.senha


def testar_setters_validos_usuario():
    u = Usuario("Joao", Cargo.Secretario, "joao@email.com", "12345678901", "1234")
    senha_anterior = u.senha

    u.nome = "  Maria Souza  "
    u.cargo = Cargo.Gestor
    u.email = "  maria@email.com  "
    u.senha = "abcd"

    assert u.nome == "Maria Souza"
    assert u.cargo == Cargo.Gestor
    assert u.email == "maria@email.com"
    assert u.cpf == "12345678901"
    assert u.senha != "abcd"
    assert u.senha != senha_anterior


def testar_erros_usuario():
    try:
        Usuario("", Cargo.Secretario, "joao@email.com", "12345678901", "1234")
        assert False, "nome deveria falhar no cadastro"
    except ValueError:
        pass

    try:
        Usuario("Joao", Cargo.Secretario, "email-invalido", "12345678901", "1234")
        assert False, "email deveria falhar no cadastro"
    except ValueError:
        pass

    try:
        Usuario("Joao", Cargo.Secretario, "joao@email.com", "123", "1234")
        assert False, "cpf deveria falhar no cadastro"
    except ValueError:
        pass

    try:
        Usuario("Joao", Cargo.Secretario, "joao@email.com", "12345678901", "12")
        assert False, "senha deveria falhar no cadastro"
    except ValueError:
        pass

    u = Usuario("Joao", Cargo.Secretario, "joao@email.com", "12345678901", "1234")

    try:
        u.nome = ""
        assert False, "nome deveria falhar"
    except ValueError:
        pass

    try:
        u.email = "email-invalido"
        assert False, "email deveria falhar"
    except ValueError:
        pass

    try:
        u.cargo = "Gestor"
        assert False, "cargo deveria falhar"
    except ValueError:
        pass

    try:
        u.senha = "12"
        assert False, "senha deveria falhar"
    except ValueError:
        pass


def testar_cadastrar_usuario():
    g = GerenciamentoUsuario()

    u = g.cadastrar_usuario(
        "Joao da Silva",
        Cargo.Gestor,
        "joao@email.com",
        "12345678901",
        "1234",
        "1234"
    )

    assert u.nome == "Joao da Silva"
    assert len(g.listar_usuarios()) == 1
    assert g.buscar_por_email("JOAO@EMAIL.COM") == u
    assert g.buscar_por_cpf("123.456.789-01") == u


def testar_nao_permitir_duplicados():
    g = GerenciamentoUsuario()

    g.cadastrar_usuario(
        "Joao da Silva",
        Cargo.Gestor,
        "joao@email.com",
        "12345678901",
        "1234",
        "1234"
    )

    try:
        g.cadastrar_usuario(
            "Maria Souza",
            Cargo.Secretario,
            "JOAO@EMAIL.COM",
            "99999999999",
            "1234",
            "1234"
        )
        assert False, "email duplicado deveria falhar"
    except ValueError:
        pass

    try:
        g.cadastrar_usuario(
            "Maria Souza",
            Cargo.Secretario,
            "maria@email.com",
            "123.456.789-01",
            "1234",
            "1234"
        )
        assert False, "cpf duplicado deveria falhar"
    except ValueError:
        pass


def testar_alterar_usuario_sem_trocar_senha():
    g = GerenciamentoUsuario()

    original = g.cadastrar_usuario(
        "Joao da Silva",
        Cargo.Secretario,
        "joao@email.com",
        "12345678901",
        "1234",
        "1234"
    )
    senha_anterior = original.senha

    u = g.alterar_usuario(
        "123.456.789-01",
        "Joao Pedro",
        Cargo.Gestor,
        "joaopedro@email.com"
    )

    assert u.nome == "Joao Pedro"
    assert u.cargo == Cargo.Gestor
    assert u.email == "joaopedro@email.com"
    assert u.cpf == "12345678901"
    assert u.senha == senha_anterior


def testar_alterar_usuario_trocando_senha():
    g = GerenciamentoUsuario()

    original = g.cadastrar_usuario(
        "Maria Souza",
        Cargo.Secretario,
        "maria@email.com",
        "99999999999",
        "1234",
        "1234"
    )
    senha_anterior = original.senha

    u = g.alterar_usuario(
        "99999999999",
        "Maria Souza Lima",
        Cargo.Secretario,
        "maria.lima@email.com",
        "4321",
        "4321"
    )

    assert u.nome == "Maria Souza Lima"
    assert u.email == "maria.lima@email.com"
    assert u.cpf == "99999999999"
    assert u.senha != senha_anterior
    assert u.senha != "4321"


def testar_buscas():
    g = GerenciamentoUsuario()

    g.cadastrar_usuario("Joao da Silva", Cargo.Gestor, "joao@email.com", "12345678901", "1234", "1234")
    g.cadastrar_usuario("Maria Souza", Cargo.Secretario, "maria@email.com", "99999999999", "1234", "1234")

    por_nome = g.buscar_por_nome("maria")
    por_cargo = g.buscar_por_cargo(Cargo.Secretario)

    assert len(por_nome) == 1
    assert por_nome[0].nome == "Maria Souza"
    assert len(por_cargo) == 1
    assert por_cargo[0].email == "maria@email.com"


def testar_excluir_usuario():
    g = GerenciamentoUsuario()

    g.cadastrar_usuario("Joao da Silva", Cargo.Gestor, "joao@email.com", "12345678901", "1234", "1234")
    g.cadastrar_usuario("Maria Souza", Cargo.Secretario, "maria@email.com", "99999999999", "1234", "1234")

    excluido = g.excluir_usuario("123.456.789-01")

    assert excluido.nome == "Joao da Silva"
    assert len(g.listar_usuarios()) == 1
    assert g.buscar_por_cpf("12345678901") is None


def rodar_testes():
    print("Rodando testes...")

    testar_criacao_usuario()
    print("criacao OK")

    testar_setters_validos_usuario()
    print("setters OK")

    testar_erros_usuario()
    print("erros OK")

    testar_cadastrar_usuario()
    print("cadastro OK")

    testar_nao_permitir_duplicados()
    print("duplicidade OK")

    testar_alterar_usuario_sem_trocar_senha()
    print("alteracao sem troca de senha OK")

    testar_alterar_usuario_trocando_senha()
    print("alteracao com troca de senha OK")

    testar_buscas()
    print("buscas OK")

    testar_excluir_usuario()
    print("exclusao OK")


if __name__ == "__main__":
    rodar_testes()

    gerenciamento = GerenciamentoUsuario()

    def listar_usuarios():
        usuarios = gerenciamento.listar_usuarios()
        if not usuarios:
            print(">> Nenhum usuario cadastrado.")
        else:
            for usuario in usuarios:
                print(
                    f"Nome: {usuario.nome} | Cargo: {usuario.cargo.name} | "
                    f"Email: {usuario.email} | CPF: {usuario.cpf}"
                )

    def ler_cargo(texto: str) -> Cargo:
        valor = input(texto)
        return Cargo(int(valor))

    def criar_usuario():
        print("\n=== Cadastrar Usuario ===")
        try:
            nome = input("Nome: ")
            cargo = ler_cargo("Cargo (1-Gestor, 2-Secretario): ")
            email = input("Email: ")
            cpf = input("CPF: ")
            senha = input("Senha: ")
            confirmar_senha = input("Confirmar senha: ")

            gerenciamento.cadastrar_usuario(nome, cargo, email, cpf, senha, confirmar_senha)
            print("Usuario cadastrado com sucesso!")
        except Exception as e:
            print(f"Erro ao cadastrar usuario: {e}")

    def editar_usuario():
        print("\n=== Alterar Usuario ===")
        try:
            cpf = input("Digite o CPF do usuario a editar: ")
            usuario = gerenciamento.buscar_por_cpf(cpf)

            if usuario is None:
                print("Usuario nao encontrado.")
                return

            print(f"CPF: {usuario.cpf} (nao pode ser alterado)")

            nome_input = input(f"Nome ({usuario.nome}): ")
            nome = nome_input.strip() if nome_input.strip() else usuario.nome

            cargo_input = input(f"Cargo ({usuario.cargo.name}) (1-Gestor, 2-Secretario): ")
            cargo = Cargo(int(cargo_input)) if cargo_input.strip() else usuario.cargo

            email_input = input(f"Email ({usuario.email}): ")
            email = email_input.strip() if email_input.strip() else usuario.email

            alterar_senha = input("Deseja alterar a senha? (s/n): ")
            if alterar_senha.lower() == "s":
                senha = input("Nova senha: ")
                confirmar_senha = input("Confirmar nova senha: ")
                gerenciamento.alterar_usuario(cpf, nome, cargo, email, senha, confirmar_senha)
            else:
                gerenciamento.alterar_usuario(cpf, nome, cargo, email)

            print("Usuario alterado com sucesso!")
        except Exception as e:
            print(f"Erro ao alterar usuario: {e}")

    def excluir_usuario():
        print("\n=== Excluir Usuario ===")
        try:
            cpf = input("Digite o CPF do usuario a excluir: ")
            usuario = gerenciamento.buscar_por_cpf(cpf)

            if usuario is None:
                print("Usuario nao encontrado.")
                return

            confirmacao = input(f"Tem certeza que deseja excluir {usuario.nome}? (s/n): ")
            if confirmacao.lower() != "s":
                print("Exclusao cancelada.")
                return

            gerenciamento.excluir_usuario(cpf)
            print("Usuario excluido com sucesso!")
        except Exception as e:
            print(f"Erro ao excluir usuario: {e}")

    while True:
        print("\n=== Tela Inicial Usuarios ===\n")
        listar_usuarios()
        print("\nOpcoes: [1] Cadastrar | [2] Editar | [3] Excluir | [4] Sair")
        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            editar_usuario()
        elif opcao == "3":
            excluir_usuario()
        elif opcao == "4":
            break
