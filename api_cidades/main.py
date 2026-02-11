from fastapi import FastAPI

app = FastAPI()

cidades_list = [
  {'id': 1, 'nome': 'Teresina', 'uf': 'PI'},
  {'id': 2, 'nome': 'Altos', 'uf': 'PI'},
  {'id': 3, 'nome': 'Coelho Neto', 'uf': 'MA'},
  {'id': 4, 'nome': 'Pedro II', 'uf': 'PI'},
]

# EndPoints (rota) de um API REST

@app.get('/cidades')
def listar_cidades():
  return cidades_list


@app.get('/cidades/{id}')
def detalhes_cidade(id: int):
  for cidade in cidades_list:
    if cidade['id'] == id:
      return cidade
  # e se não cidade


@app.delete('/cidade/{id}')
def remover_cidade(id: int):
  for index, cidade in enumerate(cidades_list):
    if cidade['id'] == id:
      cidades_list.pop(index)
      return 