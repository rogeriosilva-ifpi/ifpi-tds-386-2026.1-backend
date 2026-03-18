from pydantic import BaseModel

# Modelos
class Evento(BaseModel):
  id:int
  nome:str
  data_inicio:str
  data_fim:str
  endereco:str