from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class UsuarioBasico(BaseModel):
  id: int
  email: str
  nome: str


class Usuario(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  email: str
  senha: str
  nome: str