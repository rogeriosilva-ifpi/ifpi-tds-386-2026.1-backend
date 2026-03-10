"""
============================================================
DATABASE MODEL: EventModel
============================================================

RESPONSABILIDADE:
  Representar a tabela "events" no banco de dados.
  Este model é usado APENAS para persistência — não é
  a entidade de domínio!

DIFERENÇA ENTRE MODELS:
  1. Domain Entity (domain/entities/event_entity.py):
     - Representa o conceito de negócio
     - Python puro (dataclass)
     - Contém regras de negócio

  2. Database Model (este arquivo):
     - Representa a tabela no banco de dados
     - Herda de SQLModel (ORM)
     - Contém mapeamento coluna <-> atributo

TECNOLOGIA: SQLModel
  SQLModel unifica a definição da tabela e a validação
  de dados num só lugar.

PRINCÍPIO SOLID — SRP:
  Este arquivo tem UMA responsabilidade: mapear a
  entidade para a estrutura do banco de dados.
============================================================
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.domain.value_objects.event_type import EventType


class EventModel(SQLModel, table=True):
    """
    Model SQLModel para a tabela 'events'.

    O parâmetro `table=True` indica ao SQLModel que este
    model corresponde a uma tabela real no banco de dados.

    Cada atributo corresponde a uma coluna na tabela.
    O `Field()` permite configurar propriedades da coluna:
      - default: valor padrão
      - nullable: se a coluna aceita NULL
      - index: se deve criar índice para buscas mais rápidas
    """

    # Configuração do nome da tabela no banco
    __tablename__ = "events"

    # --- Chave Primária ---
    # Optional[int] com default=None indica autoincremento
    id: Optional[int] = Field(default=None, primary_key=True)

    # --- Campos Obrigatórios ---
    title: str = Field(index=True)          # Indexado para buscas por título
    description: str
    event_type: EventType = Field(index=True)  # Indexado para filtros por tipo
    start_date: datetime = Field(index=True)   # Indexado para filtros por período
    end_date: datetime
    location: str
    organizer: str

    # --- Campos de Auditoria ---
    # Registram quando o dado foi criado/modificado
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
