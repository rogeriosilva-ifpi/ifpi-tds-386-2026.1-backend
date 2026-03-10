"""
============================================================
CONTROLLER: EventController
============================================================

CONCEITO — Controller (Clean Architecture / MVC):
  O Controller é responsável por:
    1. Receber os dados do Request (vindos da Route)
    2. Converter Request → DTO (para a Application Layer)
    3. Chamar o Service (Application Layer)
    4. Converter Result → Response (ViewModel)
    5. Retornar o Response

RESPONSABILIDADE:
  Fazer a PONTE entre a camada HTTP (FastAPI) e a Application.
  Não contém lógica de negócio — apenas coordena o fluxo.

PRINCÍPIO SOLID — SRP:
  O Controller só cuida da "tradução" HTTP ↔ Application.
  A lógica de negócio fica no Service.
  As rotas ficam no event_routes.py.

FLUXO COMPLETO:
  HTTP Request
       ↓
  event_routes.py  (define URL, método HTTP, status code)
       ↓
  EventController  (converte Request → DTO, chama Service)
       ↓
  EventService     (caso de uso, lógica de negócio)
       ↓
  EventRepository  (interface)
       ↓
  EventRepositorySQLModel (banco de dados)
============================================================
"""

from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status

from app.application.dto.event_dto import CreateEventDTO, UpdateEventDTO
from app.application.services.event_service import EventService
from app.presentation.schemas.event_view_models import (
    EventCreateRequest,
    EventListResponse,
    EventResponse,
    EventUpdateRequest,
)


class EventController:
    """
    Controller para operações de Eventos Acadêmicos.

    Recebe o EventService via injeção de dependência.
    """

    def __init__(self, service: EventService) -> None:
        """
        Args:
            service: Instância do EventService (injetada)
        """
        self._service = service

    def create(self, request: EventCreateRequest) -> EventResponse:
        """
        Processa a criação de um novo evento.

        Converte EventCreateRequest → CreateEventDTO → chama service.
        """
        dto = CreateEventDTO(
            title=request.title,
            description=request.description,
            event_type=request.event_type,
            start_date=request.start_date,
            end_date=request.end_date,
            location=request.location,
            organizer=request.organizer,
        )

        try:
            event = self._service.create_event(dto)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )

        return EventResponse.model_validate(event.__dict__)

    def list_all(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> EventListResponse:
        """
        Processa a listagem de eventos, com filtro opcional por período.
        """
        try:
            events = self._service.list_events(start_date=start_date, end_date=end_date)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

        return EventListResponse(
            total=len(events),
            events=[EventResponse.model_validate(e.__dict__) for e in events],
        )

    def get_by_id(self, event_id: int) -> EventResponse:
        """
        Processa a busca de um evento por ID.
        """
        try:
            event = self._service.get_event(event_id)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )

        return EventResponse.model_validate(event.__dict__)

    def update(self, event_id: int, request: EventUpdateRequest) -> EventResponse:
        """
        Processa a atualização de um evento existente.
        """
        dto = UpdateEventDTO(
            title=request.title,
            description=request.description,
            event_type=request.event_type,
            start_date=request.start_date,
            end_date=request.end_date,
            location=request.location,
            organizer=request.organizer,
        )

        try:
            event = self._service.update_event(event_id, dto)
        except ValueError as e:
            # Distingue "não encontrado" de "erro de validação"
            if "não encontrado" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=str(e),
                )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )

        return EventResponse.model_validate(event.__dict__)

    def delete(self, event_id: int) -> None:
        """
        Processa a remoção de um evento.

        Retorna None — a rota responderá com 204 No Content.
        """
        try:
            self._service.delete_event(event_id)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
