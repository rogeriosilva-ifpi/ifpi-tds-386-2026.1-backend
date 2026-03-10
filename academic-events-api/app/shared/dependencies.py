"""
============================================================
INJEÇÃO DE DEPENDÊNCIAS: dependencies.py
============================================================

CONCEITO — Dependency Injection (DI):
  É um padrão onde os objetos NÃO criam suas próprias
  dependências — elas são "injetadas" de fora.

  Benefícios:
    - Facilita testes (podemos injetar mocks)
    - Desacopla as camadas
    - Centraliza a criação de objetos em um lugar

RESPONSABILIDADE:
  Este arquivo é o "fio condutor" da aplicação.
  Ele define como cada camada recebe suas dependências:

    Session (DB) → Repository → Service → Controller

TECNOLOGIA:
  FastAPI Depends() — sistema nativo de DI do FastAPI.
  Quando uma rota declara `Depends(get_event_controller)`,
  o FastAPI executa a função e injeta o resultado.

PRINCÍPIO SOLID — DIP (Dependency Inversion):
  Aqui é onde conectamos as INTERFACES às IMPLEMENTAÇÕES:
    EventRepository (interface) ← EventRepositorySQLModel (implementação)
============================================================
"""

from fastapi import Depends
from sqlmodel import Session

from app.application.services.event_service import EventService
from app.domain.repositories.event_repository import EventRepository
from app.infrastructure.database.db import get_session
from app.infrastructure.repositories.event_repository_sqlmodel import (
    EventRepositorySQLModel,
)
from app.presentation.api.controllers.event_controller import EventController


# ----------------------------------------------------------
# Provider: EventRepository
# ----------------------------------------------------------

def get_event_repository(
    session: Session = Depends(get_session),
) -> EventRepository:
    """
    Cria e retorna a implementação concreta do repositório.

    PONTO CHAVE DO DIP:
      Retorna o tipo da INTERFACE (EventRepository),
      mas instancia a IMPLEMENTAÇÃO (EventRepositorySQLModel).

      Isso significa que o código que usa esta função
      só "enxerga" a interface, nunca a implementação.

    Args:
        session: Sessão do banco (injetada automaticamente pelo FastAPI)

    Returns:
        EventRepository: implementação SQLModel
    """
    return EventRepositorySQLModel(session=session)


# ----------------------------------------------------------
# Provider: EventService
# ----------------------------------------------------------

def get_event_service(
    repository: EventRepository = Depends(get_event_repository),
) -> EventService:
    """
    Cria e retorna o EventService com o repositório injetado.

    O EventService não sabe qual repositório está usando,
    apenas que satisfaz a interface EventRepository.

    Args:
        repository: Implementação do repositório (injetada)

    Returns:
        EventService configurado
    """
    return EventService(repository=repository)


# ----------------------------------------------------------
# Provider: EventController
# ----------------------------------------------------------

def get_event_controller(
    service: EventService = Depends(get_event_service),
) -> EventController:
    """
    Cria e retorna o EventController com o serviço injetado.

    Este é o provider que as ROTAS chamam via Depends().

    Cadeia completa de injeção:
      get_session()
          ↓
      get_event_repository(session)
          ↓
      get_event_service(repository)
          ↓
      get_event_controller(service)   <-- rotas chamam este

    Args:
        service: EventService (injetado)

    Returns:
        EventController configurado
    """
    return EventController(service=service)
