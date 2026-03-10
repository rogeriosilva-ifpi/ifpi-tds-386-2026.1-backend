"""
============================================================
VIEW MODELS (Schemas): Event
============================================================

CONCEITO — ViewModel / Schema:
  ViewModels definem o formato dos dados na fronteira
  da API HTTP: o que chega no Request e o que sai no Response.

  São diferentes dos DTOs (Application Layer) porque:
    - ViewModels: lidam com JSON, validação HTTP, documentação
    - DTOs: transferem dados entre camadas internas

RESPONSABILIDADE:
  1. Definir formato do JSON de entrada (Request Body)
  2. Definir formato do JSON de saída (Response Body)
  3. Gerar documentação automática no Swagger (/docs)

TECNOLOGIA:
  Pydantic BaseModel — valida e serializa automaticamente.

CONVENÇÃO DE NOMENCLATURA:
  - EventCreateRequest: dados enviados pelo cliente para criar
  - EventUpdateRequest: dados enviados para atualizar
  - EventResponse: dados retornados pela API
  - EventListResponse: lista de eventos no response
============================================================
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator

from app.domain.value_objects.event_type import EventType


# ----------------------------------------------------------
# Schemas de Request (entrada)
# ----------------------------------------------------------

class EventCreateRequest(BaseModel):
    """
    Schema para criação de evento via POST /events.

    Todos os campos são obrigatórios.
    """

    title: str
    description: str
    event_type: EventType
    start_date: datetime
    end_date: datetime
    location: str
    organizer: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "I Congresso de Tecnologia do IFPI",
                "description": "Congresso sobre inovações em tecnologia da informação.",
                "event_type": "congress",
                "start_date": "2026-08-10T08:00:00",
                "end_date": "2026-08-12T18:00:00",
                "location": "Auditório Principal - IFPI Campus Teresina",
                "organizer": "Prof. Rogério",
            }
        }
    }

    @field_validator("title", "organizer", "location")
    @classmethod
    def must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Este campo não pode estar vazio.")
        return value.strip()

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, end_date: datetime, info) -> datetime:
        start_date = info.data.get("start_date")
        if start_date and end_date <= start_date:
            raise ValueError("A data de término deve ser posterior à data de início.")
        return end_date


class EventUpdateRequest(BaseModel):
    """
    Schema para atualização de evento via PUT /events/{id}.

    Todos os campos são opcionais (atualização parcial).
    """

    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[EventType] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    organizer: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "I Congresso de Tecnologia do IFPI - Edição Atualizada",
                "location": "Auditório B - IFPI Campus Parnaíba",
            }
        }
    }


# ----------------------------------------------------------
# Schemas de Response (saída)
# ----------------------------------------------------------

class EventResponse(BaseModel):
    """
    Schema de resposta para um único evento.

    Retornado em GET /events/{id}, POST /events, PUT /events/{id}.
    """

    id: int
    title: str
    description: str
    event_type: EventType
    start_date: datetime
    end_date: datetime
    location: str
    organizer: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        # Permite criar EventResponse a partir de objetos (não só dicts)
        # Necessário para converter Event (domain entity) → EventResponse
        "from_attributes": True
    }


class EventListResponse(BaseModel):
    """
    Schema de resposta para listagem de eventos.

    Retornado em GET /events.
    Inclui metadado de total para facilitar paginação futura.
    """

    total: int
    events: List[EventResponse]
