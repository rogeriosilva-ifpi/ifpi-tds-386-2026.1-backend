"""
============================================================
DATA TRANSFER OBJECTS (DTOs): Event
============================================================

CONCEITO — DTO (Data Transfer Object):
  DTOs são objetos simples usados para TRANSFERIR DADOS
  entre camadas da aplicação.

  Diferença em relação à Entity:
    - Entity: tem identidade, contém regras de negócio
    - DTO: transporte de dados, sem regras de negócio

RESPONSABILIDADE:
  Definir as estruturas de dados trafegadas entre:
    Presentation Layer --> Application Layer

  Isso desacopla a Application Layer dos ViewModels
  específicos do HTTP (FastAPI/Pydantic).

PRINCÍPIO SOLID — SRP:
  Cada DTO tem responsabilidade única:
    - CreateEventDTO: dados para criação
    - UpdateEventDTO: dados para atualização

NOTA: Aqui usamos Pydantic apenas para validação de tipos.
  O DTO não conhece banco de dados, HTTP ou FastAPI.
============================================================
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from app.domain.value_objects.event_type import EventType


class CreateEventDTO(BaseModel):
    """
    DTO para criação de um novo evento.

    Contém apenas os campos fornecidos pelo usuário.
    O ID, created_at e updated_at são gerados automaticamente.
    """

    title: str
    description: str
    event_type: EventType
    start_date: datetime
    end_date: datetime
    location: str
    organizer: str

    @field_validator("title", "organizer", "location")
    @classmethod
    def must_not_be_empty(cls, value: str) -> str:
        """Valida que campos de texto não sejam vazios ou só espaços."""
        if not value.strip():
            raise ValueError("Este campo não pode estar vazio.")
        return value.strip()

    @field_validator("end_date")
    @classmethod
    def end_date_must_be_after_start(cls, end_date: datetime, info) -> datetime:
        """Valida que end_date seja posterior a start_date."""
        start_date = info.data.get("start_date")
        if start_date and end_date <= start_date:
            raise ValueError("A data de término deve ser posterior à data de início.")
        return end_date


class UpdateEventDTO(BaseModel):
    """
    DTO para atualização parcial de um evento.

    Todos os campos são opcionais: o usuário envia
    apenas os campos que deseja alterar (PATCH semantics).
    """

    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[EventType] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    organizer: Optional[str] = None

    @field_validator("title", "organizer", "location")
    @classmethod
    def must_not_be_empty_if_provided(cls, value: Optional[str]) -> Optional[str]:
        """Se o campo for fornecido, não pode ser vazio."""
        if value is not None and not value.strip():
            raise ValueError("Este campo não pode estar vazio.")
        return value.strip() if value else value
