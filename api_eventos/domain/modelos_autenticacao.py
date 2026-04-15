from pydantic import BaseModel
from sqlmodel import Relationship, SQLModel, Field


class UsuarioBasico(BaseModel):
  id: int
  email: str
  nome: str


class Usuario(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  email: str
  senha: str
  nome: str

  eventos: list['Evento'] = Relationship(back_populates='usuario')