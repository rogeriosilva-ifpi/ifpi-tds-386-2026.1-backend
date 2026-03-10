"""
============================================================
IMPLEMENTAÇÃO DO REPOSITÓRIO: EventRepositorySQLModel
============================================================

RESPONSABILIDADE:
  Implementar a interface EventRepository usando SQLModel
  para persistência em banco de dados relacional.

PRINCÍPIO SOLID — DIP (Dependency Inversion Principle):
  Esta é a IMPLEMENTAÇÃO CONCRETA que satisfaz o contrato
  definido pela interface EventRepository (domain layer).

  A camada Application nunca conhece esta classe diretamente.
  Ela recebe uma instância via Dependency Injection (ver shared/dependencies.py).

PADRÃO — Repository:
  Traduz operações de domínio (create, get_by_id, etc.)
  em operações SQL usando SQLModel/SQLAlchemy.

MAPEAMENTO:
  Event (domain entity) <---> EventModel (database model)
  Esta classe é responsável por converter entre os dois.
============================================================
"""

from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, select

from app.domain.entities.event_entity import Event
from app.domain.repositories.event_repository import EventRepository
from app.domain.value_objects.event_type import EventType
from app.infrastructure.database.models.event_model import EventModel


class EventRepositorySQLModel(EventRepository):
    """
    Implementação concreta do repositório usando SQLModel.

    Recebe uma Session do banco no construtor (injeção de dependência).
    A session é gerenciada externamente (ver shared/dependencies.py).
    """

    def __init__(self, session: Session) -> None:
        """
        Args:
            session: Sessão ativa do banco de dados (injetada pelo FastAPI)
        """
        self.session = session

    # ----------------------------------------------------------
    # Métodos de Mapeamento (privados)
    # ----------------------------------------------------------

    def _to_model(self, event: Event) -> EventModel:
        """
        Converte Event (domain entity) → EventModel (ORM model).

        Necessário para salvar no banco de dados.
        """
        return EventModel(
            id=event.id,
            title=event.title,
            description=event.description,
            event_type=event.event_type,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            organizer=event.organizer,
            created_at=event.created_at,
            updated_at=event.updated_at,
        )

    def _to_entity(self, model: EventModel) -> Event:
        """
        Converte EventModel (ORM model) → Event (domain entity).

        Necessário após buscar dados do banco.
        """
        return Event(
            id=model.id,
            title=model.title,
            description=model.description,
            event_type=model.event_type,
            start_date=model.start_date,
            end_date=model.end_date,
            location=model.location,
            organizer=model.organizer,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    # ----------------------------------------------------------
    # Implementação dos métodos da interface
    # ----------------------------------------------------------

    def create(self, event: Event) -> Event:
        """
        Persiste um novo evento no banco de dados.

        Fluxo:
          1. Converte Event → EventModel
          2. Adiciona à session (INSERT preparado)
          3. Commit (executa o INSERT)
          4. Refresh (recarrega o modelo com ID gerado)
          5. Converte EventModel → Event e retorna
        """
        db_event = self._to_model(event)
        self.session.add(db_event)
        self.session.commit()
        self.session.refresh(db_event)  # Recarrega para obter o ID gerado
        return self._to_entity(db_event)

    def get_by_id(self, event_id: int) -> Optional[Event]:
        """
        Busca evento por ID.

        Retorna None se não encontrado (sem lançar exceção).
        A lógica de "404 Not Found" fica na camada Application.
        """
        db_event = self.session.get(EventModel, event_id)
        if db_event is None:
            return None
        return self._to_entity(db_event)

    def list_all(self) -> List[Event]:
        """
        Lista todos os eventos ordenados por data de início.

        O `select(EventModel)` gera: SELECT * FROM events
        """
        statement = select(EventModel).order_by(EventModel.start_date)
        results = self.session.exec(statement).all()
        return [self._to_entity(model) for model in results]

    def list_by_period(self, start_date: datetime, end_date: datetime) -> List[Event]:
        """
        Lista eventos dentro do período especificado.

        SQL gerado (aproximado):
          SELECT * FROM events
          WHERE start_date >= :start_date AND start_date <= :end_date
          ORDER BY start_date
        """
        statement = (
            select(EventModel)
            .where(EventModel.start_date >= start_date)
            .where(EventModel.start_date <= end_date)
            .order_by(EventModel.start_date)
        )
        results = self.session.exec(statement).all()
        return [self._to_entity(model) for model in results]

    def update(self, event: Event) -> Event:
        """
        Atualiza um evento existente no banco de dados.

        Fluxo:
          1. Busca o EventModel pelo ID
          2. Atualiza os campos modificados
          3. Commit
          4. Refresh
          5. Retorna a entidade atualizada
        """
        db_event = self.session.get(EventModel, event.id)
        if db_event is None:
            raise ValueError(f"Evento com id={event.id} não encontrado para atualização.")

        # Atualiza os campos do model com os valores da entidade
        db_event.title = event.title
        db_event.description = event.description
        db_event.event_type = event.event_type
        db_event.start_date = event.start_date
        db_event.end_date = event.end_date
        db_event.location = event.location
        db_event.organizer = event.organizer
        db_event.updated_at = event.updated_at

        self.session.add(db_event)
        self.session.commit()
        self.session.refresh(db_event)
        return self._to_entity(db_event)

    def delete(self, event_id: int) -> bool:
        """
        Remove evento pelo ID.

        Returns:
            True se removido, False se não encontrado
        """
        db_event = self.session.get(EventModel, event_id)
        if db_event is None:
            return False

        self.session.delete(db_event)
        self.session.commit()
        return True
