"""
============================================================
CONFIGURAÇÃO DE TESTES: conftest.py
============================================================

RESPONSABILIDADE:
  Definir fixtures compartilhadas entre todos os testes.

CONCEITO — Fixture (pytest):
  Uma fixture é uma função que fornece dados ou objetos
  para os testes. É executada antes do teste e pode
  fazer limpeza após (com yield).

CONCEITO — Test Isolation:
  Cada teste deve rodar em isolamento, sem depender de
  estado deixado por testes anteriores.
  Usamos um banco SQLite em memória (:memory:) para isso.

ESTRATÉGIA DE TESTES:
  - Banco de dados: SQLite em memória (apagado após cada teste)
  - Repositório: implementação real (não mock) para testes de integração
  - Service: testado com repositório real
  - API: testado com TestClient do FastAPI
============================================================
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from app.infrastructure.database.db import get_session
from app.infrastructure.repositories.event_repository_sqlmodel import (
    EventRepositorySQLModel,
)
from app.application.services.event_service import EventService


# ----------------------------------------------------------
# Fixture: Banco de dados em memória para testes
# ----------------------------------------------------------

@pytest.fixture(name="session")
def session_fixture():
    """
    Cria um banco SQLite em memória para cada teste.

    O banco é criado antes do teste e destruído após.
    Garante que cada teste começa com o banco limpo.

    StaticPool: mantém a mesma conexão durante o teste
    (necessário para SQLite em memória).
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


# ----------------------------------------------------------
# Fixture: Repositório com sessão de teste
# ----------------------------------------------------------

@pytest.fixture(name="repository")
def repository_fixture(session: Session):
    """
    Cria um repositório usando a sessão de teste (banco em memória).
    """
    return EventRepositorySQLModel(session=session)


# ----------------------------------------------------------
# Fixture: Service com repositório de teste
# ----------------------------------------------------------

@pytest.fixture(name="service")
def service_fixture(repository: EventRepositorySQLModel):
    """
    Cria um EventService com o repositório de teste injetado.
    """
    return EventService(repository=repository)


# ----------------------------------------------------------
# Fixture: TestClient da API com banco em memória
# ----------------------------------------------------------

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Cria um TestClient do FastAPI substituindo a sessão real
    pela sessão de teste (banco em memória).

    Isso é feito sobrescrevendo a dependência `get_session`
    com uma versão que usa o banco de teste.
    """

    def get_session_override():
        yield session

    # Sobrescreve a dependência de sessão
    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        yield client

    # Limpa o override após o teste
    app.dependency_overrides.clear()
