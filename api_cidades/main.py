from fastapi import FastAPI
from pydantic import BaseModel

# Application FastAPI 
app = FastAPI()


# Modelos Pydantic (Objeto) - Schemas ou ViewModels
class Cidade(BaseModel):
  id: int 
  nome: str
  uf: str


class NovaCidade(BaseModel):
  nome: str
  uf: str

# Banco de Dados (Fake)
proximo_id = 1
cidades = []


# Endpoints (Controllers)
@app.get('/cidades')
def cidades_list():
  return cidades


@app.post('/cidades', status_code=201)
def cidades_create(nova_cidade: NovaCidade):
  global proximo_id
  cidade = Cidade(id=proximo_id, 
                  nome=nova_cidade.nome, 
                  uf=nova_cidade.uf)
  proximo_id += 1

  cidades.append(cidade)
  return cidade


@app.get('/cidades/{id}')
def cidades_detail(id: int):
  for cidade in cidades:
    if cidade.id == id:
      return cidade
  
  return f'Não existe cidade com id --> {id}'


