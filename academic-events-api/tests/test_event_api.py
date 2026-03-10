"""
============================================================
TESTES: Event API (Camada de Presentation)
============================================================

ESTRATÉGIA:
  Testa os endpoints HTTP usando TestClient do FastAPI.
  O banco de dados real é substituído por SQLite em memória
  via dependency override (ver conftest.py).

  Estes são testes de INTEGRAÇÃO: testam todo o fluxo
  HTTP → Controller → Service → Repository → DB.
============================================================
"""

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient


# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------

def make_event_payload(**overrides) -> dict:
    """Cria payload JSON válido para criação de evento."""
    now = datetime.utcnow()
    defaults = {
        "title": "Seminário de Python",
        "description": "Introdução à linguagem Python",
        "event_type": "seminar",
        "start_date": (now + timedelta(days=5)).isoformat(),
        "end_date": (now + timedelta(days=5, hours=3)).isoformat(),
        "location": "Sala 101 - IFPI",
        "organizer": "Prof. Rogério",
    }
    defaults.update(overrides)
    return defaults


# ----------------------------------------------------------
# Testes: Health Check
# ----------------------------------------------------------

class TestHealthCheck:

    def test_health_check_returns_ok(self, client: TestClient):
        """O endpoint /health deve retornar status ok."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


# ----------------------------------------------------------
# Testes: POST /events
# ----------------------------------------------------------

class TestCreateEventAPI:

    def test_create_event_returns_201(self, client: TestClient):
        """Criação bem-sucedida deve retornar 201 Created."""
        response = client.post("/events/", json=make_event_payload())
        assert response.status_code == 201

    def test_create_event_returns_event_with_id(self, client: TestClient):
        """Response deve conter o evento criado com ID."""
        response = client.post("/events/", json=make_event_payload())
        data = response.json()

        assert "id" in data
        assert data["id"] > 0
        assert data["title"] == "Seminário de Python"
        assert data["event_type"] == "seminar"

    def test_create_event_missing_field_returns_422(self, client: TestClient):
        """Campos obrigatórios ausentes devem retornar 422."""
        payload = make_event_payload()
        del payload["title"]  # Remove campo obrigatório

        response = client.post("/events/", json=payload)
        assert response.status_code == 422


# ----------------------------------------------------------
# Testes: GET /events
# ----------------------------------------------------------

class TestListEventsAPI:

    def test_list_events_empty(self, client: TestClient):
        """Lista vazia quando não há eventos."""
        response = client.get("/events/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["events"] == []

    def test_list_events_returns_all(self, client: TestClient):
        """Retorna todos os eventos criados."""
        client.post("/events/", json=make_event_payload(title="Evento 1"))
        client.post("/events/", json=make_event_payload(title="Evento 2"))

        response = client.get("/events/")
        data = response.json()

        assert data["total"] == 2
        assert len(data["events"]) == 2

    def test_list_events_filter_by_period(self, client: TestClient):
        """Filtra eventos por período via query params."""
        # Cria evento em agosto de 2026
        client.post("/events/", json=make_event_payload(
            title="Evento Agosto",
            start_date="2026-08-10T08:00:00",
            end_date="2026-08-10T18:00:00",
        ))
        # Cria evento em outubro de 2026
        client.post("/events/", json=make_event_payload(
            title="Evento Outubro",
            start_date="2026-10-05T08:00:00",
            end_date="2026-10-05T18:00:00",
        ))

        # Filtra apenas agosto
        response = client.get(
            "/events/",
            params={
                "start_date": "2026-08-01T00:00:00",
                "end_date": "2026-08-31T23:59:59",
            },
        )
        data = response.json()

        assert data["total"] == 1
        assert data["events"][0]["title"] == "Evento Agosto"


# ----------------------------------------------------------
# Testes: GET /events/{id}
# ----------------------------------------------------------

class TestGetEventAPI:

    def test_get_event_success(self, client: TestClient):
        """Busca evento existente retorna 200."""
        create_response = client.post("/events/", json=make_event_payload())
        event_id = create_response.json()["id"]

        response = client.get(f"/events/{event_id}")
        assert response.status_code == 200
        assert response.json()["id"] == event_id

    def test_get_event_not_found(self, client: TestClient):
        """Evento inexistente deve retornar 404."""
        response = client.get("/events/9999")
        assert response.status_code == 404


# ----------------------------------------------------------
# Testes: PUT /events/{id}
# ----------------------------------------------------------

class TestUpdateEventAPI:

    def test_update_event_success(self, client: TestClient):
        """Atualiza evento e retorna dados atualizados."""
        create_response = client.post("/events/", json=make_event_payload())
        event_id = create_response.json()["id"]

        response = client.put(
            f"/events/{event_id}",
            json={"title": "Título Atualizado"},
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Título Atualizado"

    def test_update_event_not_found(self, client: TestClient):
        """Atualizar evento inexistente deve retornar 404."""
        response = client.put("/events/9999", json={"title": "Novo"})
        assert response.status_code == 404


# ----------------------------------------------------------
# Testes: DELETE /events/{id}
# ----------------------------------------------------------

class TestDeleteEventAPI:

    def test_delete_event_success(self, client: TestClient):
        """Remove evento existente retorna 204 No Content."""
        create_response = client.post("/events/", json=make_event_payload())
        event_id = create_response.json()["id"]

        response = client.delete(f"/events/{event_id}")
        assert response.status_code == 204

    def test_delete_event_removes_from_list(self, client: TestClient):
        """Após remover, evento não deve aparecer na listagem."""
        create_response = client.post("/events/", json=make_event_payload())
        event_id = create_response.json()["id"]

        client.delete(f"/events/{event_id}")

        list_response = client.get("/events/")
        assert list_response.json()["total"] == 0

    def test_delete_event_not_found(self, client: TestClient):
        """Remover evento inexistente deve retornar 404."""
        response = client.delete("/events/9999")
        assert response.status_code == 404
