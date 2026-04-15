from sqlmodel import Field, Relationship, SQLModel

from domain.modelos_autenticacao import Usuario

# Modelos
class Evento(SQLModel, table=True):
  id:int | None = Field(default=None, primary_key=True)
  nome:str
  data_inicio:str
  data_fim:str | None = None
  endereco:str | None = None

  usuario_id: int | None = Field(foreign_key='usuario.id')
  usuario: Usuario | None = Relationship(back_populates='eventos')