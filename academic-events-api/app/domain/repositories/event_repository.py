"""
============================================================
INTERFACE DO REPOSITÓRIO: EventRepository
============================================================

CONCEITO — Repository Pattern (DDD):
  O repositório é uma abstração que representa uma coleção
  de entidades. Ele esconde os detalhes de persistência
  (banco de dados, arquivos, etc.) do domínio.

PRINCÍPIO SOLID — DIP (Dependency Inversion Principle):
  Esta é a ABSTRAÇÃO (interface) que define o contrato.
  A camada de Application depende DESTA interface,
  não da implementação concreta (SQL, etc.).

  Diagrama de dependências:
    Application Service --> EventRepository (interface)  <-- AQUI
                                    ^
                                    |
                        EventRepositorySQLModel (implementação)
                        (definida na camada Infrastructure)

IMPORTANTE:
  Este arquivo não importa nada de SQLModel, banco de dados
  ou qualquer framework. É Python puro com ABC!
============================================================
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from app.domain.entities.event_entity import Event


class EventRepository(ABC):
    """
    Interface abstrata para o repositório de Eventos.

    Define o CONTRATO que qualquer implementação de persistência
    deve seguir. Seja SQLite, PostgreSQL, MongoDB ou até memória.

    Todos os métodos são abstratos — obrigam a implementação.
    """

    @abstractmethod
    def create(self, event: Event) -> Event:
        """
        Persiste um novo evento e retorna a entidade com ID gerado.

        Args:
            event: Entidade Event sem ID (ainda não persistida)

        Returns:
            Event: Entidade com ID preenchido após persistência
        """
        ...

    @abstractmethod
    def get_by_id(self, event_id: int) -> Optional[Event]:
        """
        Busca um evento pelo seu ID.

        Args:
            event_id: Identificador único do evento

        Returns:
            Event se encontrado, None se não existir
        """
        ...

    @abstractmethod
    def list_all(self) -> List[Event]:
        """
        Retorna todos os eventos cadastrados.

        Returns:
            Lista de entidades Event
        """
        ...

    @abstractmethod
    def list_by_period(self, start_date: datetime, end_date: datetime) -> List[Event]:
        """
        Retorna eventos que ocorrem dentro do período especificado.

        Args:
            start_date: Data de início do filtro
            end_date: Data de término do filtro

        Returns:
            Lista de eventos no período
        """
        ...

    @abstractmethod
    def update(self, event: Event) -> Event:
        """
        Atualiza um evento existente no repositório.

        Args:
            event: Entidade Event com dados atualizados e ID preenchido

        Returns:
            Event atualizado
        """
        ...

    @abstractmethod
    def delete(self, event_id: int) -> bool:
        """
        Remove um evento pelo ID.

        Args:
            event_id: Identificador único do evento a remover

        Returns:
            True se removido com sucesso, False se não encontrado
        """
        ...
