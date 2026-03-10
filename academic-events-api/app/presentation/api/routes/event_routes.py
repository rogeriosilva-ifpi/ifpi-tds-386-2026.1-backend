"""
============================================================
ROTAS: Event Routes
============================================================

RESPONSABILIDADE:
  Definir os endpoints HTTP da API de Eventos:
    - URL (path)
    - Método HTTP (GET, POST, PUT, DELETE)
    - Status code de sucesso
    - Tipos de entrada e saída (para documentação automática)
    - Dependências (injeção de dependências do FastAPI)

PRINCÍPIO SOLID — SRP:
  Este arquivo só cuida de ROTEAMENTO.
  A lógica de processamento fica no EventController.

TECNOLOGIA:
  APIRouter do FastAPI — permite organizar rotas em módulos
  e depois registrá-las no main.py com um prefixo.

DOCUMENTAÇÃO AUTOMÁTICA:
  O FastAPI gera automaticamente o Swagger UI (/docs)
  e ReDoc (/redoc) a partir destes decoradores.
============================================================
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, status

from app.presentation.api.controllers.event_controller import EventController
from app.presentation.schemas.event_view_models import (
    EventCreateRequest,
    EventListResponse,
    EventResponse,
    EventUpdateRequest,
)
from app.shared.dependencies import get_event_controller

# Criação do router com prefixo e tag para documentação
router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


# ----------------------------------------------------------
# POST /events — Criar novo evento
# ----------------------------------------------------------
@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo evento acadêmico",
    description="Cadastra um novo evento acadêmico no sistema.",
)
def create_event(
    request: EventCreateRequest,
    controller: EventController = Depends(get_event_controller),
):
    """
    Cria um novo evento acadêmico.

    - **title**: Título do evento
    - **description**: Descrição detalhada
    - **event_type**: Tipo (congress, seminar, workshop, lecture, short_course, symposium, other)
    - **start_date**: Data/hora de início (ISO 8601)
    - **end_date**: Data/hora de término (ISO 8601)
    - **location**: Local do evento
    - **organizer**: Nome do organizador
    """
    return controller.create(request)


# ----------------------------------------------------------
# GET /events — Listar eventos (com filtro opcional por período)
# ----------------------------------------------------------
@router.get(
    "/",
    response_model=EventListResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar eventos acadêmicos",
    description="Retorna todos os eventos. Filtre por período usando start_date e end_date.",
)
def list_events(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    controller: EventController = Depends(get_event_controller),
):
    """
    Lista todos os eventos cadastrados.

    Filtros opcionais via query parameters:
    - **start_date**: Início do período (ex: 2026-08-01T00:00:00)
    - **end_date**: Fim do período (ex: 2026-08-31T23:59:59)
    """
    return controller.list_all(start_date=start_date, end_date=end_date)


# ----------------------------------------------------------
# GET /events/{id} — Buscar evento por ID
# ----------------------------------------------------------
@router.get(
    "/{event_id}",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar evento por ID",
    description="Retorna os dados de um evento específico pelo seu ID.",
)
def get_event(
    event_id: int,
    controller: EventController = Depends(get_event_controller),
):
    return controller.get_by_id(event_id)


# ----------------------------------------------------------
# PUT /events/{id} — Atualizar evento
# ----------------------------------------------------------
@router.put(
    "/{event_id}",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualizar evento acadêmico",
    description="Atualiza os dados de um evento. Envie apenas os campos que deseja alterar.",
)
def update_event(
    event_id: int,
    request: EventUpdateRequest,
    controller: EventController = Depends(get_event_controller),
):
    return controller.update(event_id, request)


# ----------------------------------------------------------
# DELETE /events/{id} — Remover evento
# ----------------------------------------------------------
@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover evento acadêmico",
    description="Remove permanentemente um evento do sistema.",
)
def delete_event(
    event_id: int,
    controller: EventController = Depends(get_event_controller),
):
    controller.delete(event_id)
