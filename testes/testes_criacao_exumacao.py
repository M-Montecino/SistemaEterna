    
def __criar_sepultamentos_teste(self) -> list[Sepultamento]:
        # Esta lista substitui temporariamente a busca no ControladorSepultamento,
        # permitindo testar sepultamentos elegiveis e nao elegiveis para exumacao.
        hoje = datetime.now()

        def criar_sepultamento(
            cpf_falecido: str,
            nome_falecido: str,
            codigo_tumulo: int,
            setor: str,
            numero_tumulo: int,
            data_final_cons: datetime,
            observacoes: str
        ) -> Sepultamento:
            data_nascimento = datetime.strptime("01/01/1940", "%d/%m/%Y")
            data_falecimento = data_final_cons - timedelta(days=365)
            data_sepultamento = data_falecimento + timedelta(days=2)
            data_inicio_cons = data_final_cons - timedelta(days=5 * 365)
            data_pagamento = data_inicio_cons

            return Sepultamento(
                cpf_falecido=cpf_falecido,
                nome_falecido=nome_falecido,
                data_nascimento=data_nascimento,
                data_falecimento=data_falecimento,
                causa_morte="Causas naturais",
                tumulo=Tumulo(
                    codigo=codigo_tumulo,
                    setor=setor,
                    numero=numero_tumulo,
                    tipo=TipoTumulo.Gaveteiro,
                    capacidade=2
                ),
                valor=2500.00,
                data_pagamento=data_pagamento,
                tipo_pagamento="PIX",
                responsavel="479.768.520-43",
                responsavel2="310.531.250-11",
                data_inicio_cons=data_inicio_cons,
                data_final_cons=data_final_cons,
                status=2,
                data_sepultamento=data_sepultamento,
                observacoes=observacoes
            )

        return [
            criar_sepultamento(
                cpf_falecido="794.880.230-40",
                nome_falecido="Carlos Pereira",
                codigo_tumulo=1,
                setor="A",
                numero_tumulo=12,
                data_final_cons=hoje - timedelta(days=90),
                observacoes=(
                    "Elegivel: concessao vencida ha 90 dias."
                )
            ),
            criar_sepultamento(
                cpf_falecido="529.982.247-25",
                nome_falecido="Maria Oliveira",
                codigo_tumulo=2,
                setor="A",
                numero_tumulo=18,
                data_final_cons=hoje - timedelta(days=31),
                observacoes=(
                    "Elegivel: concessao vencida ha 31 dias."
                )
            ),
            criar_sepultamento(
                cpf_falecido="111.444.777-35",
                nome_falecido="Joao Almeida",
                codigo_tumulo=3,
                setor="B",
                numero_tumulo=7,
                data_final_cons=hoje - timedelta(days=30),
                observacoes=(
                    "Elegivel no limite: data_final_cons + 30 dias ja chegou."
                )
            ),
            criar_sepultamento(
                cpf_falecido="123.456.789-09",
                nome_falecido="Ana Souza",
                codigo_tumulo=4,
                setor="B",
                numero_tumulo=21,
                data_final_cons=hoje - timedelta(days=15),
                observacoes=(
                    "Nao elegivel: concessao vencida ha apenas 15 dias."
                )
            ),
            criar_sepultamento(
                cpf_falecido="987.654.321-00",
                nome_falecido="Pedro Santos",
                codigo_tumulo=5,
                setor="C",
                numero_tumulo=4,
                data_final_cons=hoje + timedelta(days=60),
                observacoes=(
                    "Nao elegivel: concessao ainda nao venceu."
                )
            ),
            criar_sepultamento(
                cpf_falecido="390.533.447-05",
                nome_falecido="Helena Costa",
                codigo_tumulo=6,
                setor="C",
                numero_tumulo=30,
                data_final_cons=hoje - timedelta(days=365),
                observacoes=(
                    "Elegivel: concessao vencida ha aproximadamente 1 ano."
                )
            )
        ]