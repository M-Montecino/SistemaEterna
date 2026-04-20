#este arquivo será excluido posteriormente

from datetime import datetime
from manutencao import Manutencao, TipoServico

m = Manutencao(
    codigo=1,
    tumulo="A1",
    tipo_servico=TipoServico.Limpeza,
    data=datetime.now(),
    cpf_responsavel="12345678900"
)

print("--- TESTE DE CRIAÇÃO ---")
print(m.codigo)
print(m.tumulo)
print(m.tipo_servico)
print(m.data)
print(m.cpf_responsavel)

print("\n--- TESTE DE ALTERAÇÃO ---")
m.codigo = 2
m.tipo_servico = TipoServico.Reparo

print(m.codigo)
print(m.tipo_servico)

print("\n--- TESTE DE ERRO ---")
try:
    m.codigo = "errado"
except ValueError as e:
    print("Erro capturado:", e)