from pydantic import BaseModel


class UsuarioBasico(BaseModel):
  id: int
  email: str
  nome: str


class Usuario(BaseModel):
  id: int
  email: str
  senha: str
  nome: str