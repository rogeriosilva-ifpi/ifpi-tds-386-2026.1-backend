"""
============================================================
TESTES: EventService (Camada de Application)
============================================================

ESTRATÉGIA:
  Testa os casos de uso do EventService diretamente,
  sem passar pelo HTTP. Usa repositório real com banco
  SQLite em memória.

NOMENCLATURA:
  test_<método>_<cenário>()
  Ex: test_create_event_success, test_create_event_invalid_dates
============================================================
"""

from datetime import datetime, timedelta

import pytest

from app.application.dto.event_dto import CreateEventDTO, UpdateEventDTO
from app.application.services.event_service import EventService
from app.domain.value_objects.event_type import EventType


# ----------------------------------------------------------
# Helpers (dados de teste)
# ----------------------------------------------------------

def make_create_dto(**overrides) -> CreateEventDTO:
    """
    Cria um CreateEventDTO com dados válidos.
    Use overrides para personalizar campos específicos.
    """
    now = datetime.utcnow()
    defaults = {
        "title": "Workshop de FastAPI",
        "description": "Introdução ao FastAPI com Python",
        "event_type": EventType.WORKSHOP,
        "start_date": now + timedelta(days=10),
        "end_date": now + timedelta(days=10, hours=4),
        "location": "Laboratório 01 - IFPI",
        "organizer": "Prof. Rogério",
    }
    defaults.update(overrides)
    return CreateEventDTO(**defaults)


# ----------------------------------------------------------
# Testes: Criar Evento
# ----------------------------------------------------------

class TestCreateEvent:

    def test_create_event_success(self, service: EventService):
        """Cenário feliz: cria evento com dados válidos."""
        dto = make_create_dto()
        event = service.create_event(dto)

        assert event.id is not None
        assert event.id > 0
        assert event.title == dto.title
        assert event.organizer == dto.organizer
        assert event.event_type == EventType.WORKSHOP

    def test_create_event_returns_with_id(self, service: EventService):
        """Garante que o evento retornado tem ID gerado pelo banco."""
        dto = make_create_dto()
        event = service.create_event(dto)
        assert event.id is not None

    def test_create_event_invalid_dates(self, service: EventService):
        """Erro: data de término antes da data de início."""
        now = datetime.utcnow()
        with pytest.raises(ValueError, match="data de início"):
            service.create_event(make_create_dto(
                start_date=now + timedelta(days=5),
                end_date=now + timedelta(days=1),  # antes do início!
            ))


# ----------------------------------------------------------
# Testes: Listar Eventos
# ----------------------------------------------------------

class TestListEvents:

    def test_list_all_empty(self, service: EventService):
        """Retorna lista vazia quando não há eventos."""
        events = service.list_events()
        assert events == []

    def test_list_all_returns_created_events(self, service: EventService):
        """Retorna todos os eventos criados."""
        service.create_event(make_create_dto(title="Evento 1"))
        service.create_event(make_create_dto(title="Evento 2"))
        service.create_event(make_create_dto(title="Evento 3"))

        events = service.list_events()
        assert len(events) == 3

    def test_list_by_period_filters_correctly(self, service: EventService):
        """Filtra eventos dentro do período especificado."""
        now = datetime.utcnow()

        # Evento em agosto
        service.create_event(make_create_dto(
            title="Evento Agosto",
            start_date=datetime(2026, 8, 10),
            end_date=datetime(2026, 8, 11),
        ))

        # Evento em setembro
        service.create_event(make_create_dto(
            title="Evento Setembro",
            start_date=datetime(2026, 9, 5),
            end_date=datetime(2026, 9, 6),
        ))

        # Filtra apenas agosto
        events = service.list_events(
            start_date=datetime(2026, 8, 1),
            end_date=datetime(2026, 8, 31),
        )

        assert len(events) == 1
        assert events[0].title == "Evento Agosto"

    def test_list_by_period_invalid_range(self, service: EventService):
        """Erro: data de início do filtro maior que data de término."""
        with pytest.raises(ValueError):
            service.list_events(
                start_date=datetime(2026, 9, 1),
                end_date=datetime(2026, 8, 1),  # anterior!
            )


# ----------------------------------------------------------
# Testes: Buscar por ID
# ----------------------------------------------------------

class TestGetEvent:

    def test_get_event_success(self, service: EventService):
        """Busca evento existente pelo ID."""
        created = service.create_event(make_create_dto())
        found = service.get_event(created.id)

        assert found.id == created.id
        assert found.title == created.title

    def test_get_event_not_found(self, service: EventService):
        """Erro: evento com ID inexistente."""
        with pytest.raises(ValueError, match="não encontrado"):
            service.get_event(9999)


# ----------------------------------------------------------
# Testes: Atualizar Evento
# ----------------------------------------------------------

class TestUpdateEvent:

    def test_update_event_title(self, service: EventService):
        """Atualiza apenas o título do evento."""
        created = service.create_event(make_create_dto())

        dto = UpdateEventDTO(title="Título Atualizado")
        updated = service.update_event(created.id, dto)

        assert updated.id == created.id
        assert updated.title == "Título Atualizado"
        assert updated.organizer == created.organizer  # não mudou

    def test_update_event_not_found(self, service: EventService):
        """Erro: tentar atualizar evento inexistente."""
        with pytest.raises(ValueError, match="não encontrado"):
            service.update_event(9999, UpdateEventDTO(title="Novo"))


# ----------------------------------------------------------
# Testes: Remover Evento
# ----------------------------------------------------------

class TestDeleteEvent:

    def test_delete_event_success(self, service: EventService):
        """Remove evento existente."""
        created = service.create_event(make_create_dto())
        service.delete_event(created.id)

        # Verifica que o evento não existe mais
        with pytest.raises(ValueError, match="não encontrado"):
            service.get_event(created.id)

    def test_delete_event_not_found(self, service: EventService):
        """Erro: tentar remover evento inexistente."""
        with pytest.raises(ValueError, match="não encontrado"):
            service.delete_event(9999)
