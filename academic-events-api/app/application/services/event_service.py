"""
============================================================
APPLICATION SERVICE: EventService
============================================================

CONCEITO — Application Service (Clean Architecture):
  O Service implementa os CASOS DE USO da aplicação.
  É a camada que orquestra o fluxo entre Presentation e Domain.

RESPONSABILIDADE:
  Coordenar a execução dos casos de uso:
    - Criar evento
    - Listar eventos
    - Buscar evento por ID
    - Filtrar eventos por período
    - Atualizar evento
    - Remover evento

PRINCÍPIO SOLID — DIP (Dependency Inversion Principle):
  Este serviço depende da INTERFACE EventRepository,
  não da implementação concreta (SQLModel, memória, etc.).

  Isso significa que posso trocar o banco de dados sem
  alterar uma linha do EventService!

PRINCÍPIO SOLID — SRP (Single Responsibility Principle):
  Este serviço tem UMA responsabilidade: implementar
  os casos de uso relacionados a Eventos.

O QUE O SERVICE NÃO FAZ:
  - Não conhece SQL ou banco de dados
  - Não conhece FastAPI, HTTP ou JSON
  - Não conhece detalhes de infraestrutura
============================================================
"""

from datetime import datetime
from typing import List, Optional

from app.application.dto.event_dto import CreateEventDTO, UpdateEventDTO
from app.domain.entities.event_entity import Event
from app.domain.repositories.event_repository import EventRepository


class EventService:
    """
    Serviço de aplicação para gerenciamento de Eventos Acadêmicos.

    Recebe o repositório via injeção de dependência no construtor.
    Não instancia nem conhece a implementação concreta do repositório.
    """

    def __init__(self, repository: EventRepository) -> None:
        """
        Args:
            repository: Implementação de EventRepository (injetada)
                        Pode ser EventRepositorySQLModel, EventRepositoryInMemory, etc.
        """
        # NOTA: O tipo declarado é a INTERFACE (EventRepository),
        # não a implementação. Isso é o DIP em ação.
        self._repository = repository

    # ----------------------------------------------------------
    # Caso de Uso 1: Criar Evento
    # ----------------------------------------------------------

    def create_event(self, dto: CreateEventDTO) -> Event:
        """
        Caso de uso: Cadastrar um novo evento acadêmico.

        Fluxo:
          1. Converte DTO → Entity (domain object)
          2. Valida as regras de negócio
          3. Persiste via repositório
          4. Retorna a entidade criada (com ID)

        Args:
            dto: Dados do evento a criar (sem ID)

        Returns:
            Event: Evento criado com ID preenchido
        """
        # Cria a entidade de domínio a partir do DTO
        event = Event(
            title=dto.title,
            description=dto.description,
            event_type=dto.event_type,
            start_date=dto.start_date,
            end_date=dto.end_date,
            location=dto.location,
            organizer=dto.organizer,
        )

        # Valida as regras de negócio da entidade
        event.validate()

        # Delega a persistência ao repositório (sem conhecer detalhes)
        return self._repository.create(event)

    # ----------------------------------------------------------
    # Caso de Uso 2: Listar Eventos
    # ----------------------------------------------------------

    def list_events(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Event]:
        """
        Caso de uso: Listar eventos, com filtro opcional por período.

        Se start_date e end_date forem fornecidos, filtra por período.
        Caso contrário, retorna todos os eventos.

        Args:
            start_date: Início do filtro de período (opcional)
            end_date: Fim do filtro de período (opcional)

        Returns:
            Lista de eventos
        """
        if start_date and end_date:
            if start_date > end_date:
                raise ValueError(
                    "A data de início do filtro deve ser anterior à data de término."
                )
            return self._repository.list_by_period(start_date, end_date)

        return self._repository.list_all()

    # ----------------------------------------------------------
    # Caso de Uso 3: Buscar Evento por ID
    # ----------------------------------------------------------

    def get_event(self, event_id: int) -> Event:
        """
        Caso de uso: Buscar um evento específico pelo ID.

        Args:
            event_id: ID do evento

        Returns:
            Event: Evento encontrado

        Raises:
            ValueError: Se o evento não for encontrado
        """
        event = self._repository.get_by_id(event_id)
        if event is None:
            raise ValueError(f"Evento com id={event_id} não encontrado.")
        return event

    # ----------------------------------------------------------
    # Caso de Uso 4: Atualizar Evento
    # ----------------------------------------------------------

    def update_event(self, event_id: int, dto: UpdateEventDTO) -> Event:
        """
        Caso de uso: Atualizar os dados de um evento existente.

        Fluxo:
          1. Busca o evento (lança erro se não encontrar)
          2. Aplica as atualizações na entidade (via Event.update())
          3. Persiste via repositório

        Args:
            event_id: ID do evento a atualizar
            dto: Campos a atualizar (apenas os não-None serão alterados)

        Returns:
            Event: Evento atualizado
        """
        # Busca o evento atual (já valida existência)
        event = self.get_event(event_id)

        # Delega a atualização para a própria entidade
        # A entidade conhece suas regras, o service apenas coordena
        event.update(
            title=dto.title,
            description=dto.description,
            event_type=dto.event_type,
            start_date=dto.start_date,
            end_date=dto.end_date,
            location=dto.location,
            organizer=dto.organizer,
        )

        return self._repository.update(event)

    # ----------------------------------------------------------
    # Caso de Uso 5: Remover Evento
    # ----------------------------------------------------------

    def delete_event(self, event_id: int) -> None:
        """
        Caso de uso: Remover um evento pelo ID.

        Args:
            event_id: ID do evento a remover

        Raises:
            ValueError: Se o evento não for encontrado
        """
        # Verifica existência antes de tentar deletar
        self.get_event(event_id)

        deleted = self._repository.delete(event_id)
        if not deleted:
            raise ValueError(f"Falha ao remover evento com id={event_id}.")
