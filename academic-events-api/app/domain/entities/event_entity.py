"""
============================================================
ENTITY: Event
============================================================

CONCEITO — Entity (DDD):
  Uma Entity é um objeto do domínio com IDENTIDADE própria.
  Dois eventos são diferentes mesmo que tenham os mesmos
  atributos, pois cada um tem um ID único.

RESPONSABILIDADE:
  Representar o conceito de "Evento Acadêmico" no domínio,
  com suas regras e validações de negócio.

PRINCÍPIO SOLID — SRP (Single Responsibility):
  Esta classe tem UMA responsabilidade: representar
  a entidade Evento no domínio de negócio.

IMPORTANTE:
  Esta classe NÃO herda de SQLModel, NÃO usa FastAPI.
  É Python puro com dataclass — agnóstica a frameworks!
  Isso garante que o domínio seja independente de tecnologia.
============================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.domain.value_objects.event_type import EventType


@dataclass
class Event:
    """
    Entidade de domínio representando um Evento Acadêmico.

    Campos:
      - id: identificador único (None quando ainda não persistido)
      - title: título do evento
      - description: descrição detalhada
      - event_type: tipo do evento (Value Object EventType)
      - start_date: data/hora de início
      - end_date: data/hora de término
      - location: local do evento
      - organizer: responsável pela organização
      - created_at: data de criação do registro
      - updated_at: data da última atualização
    """

    title: str
    description: str
    event_type: EventType
    start_date: datetime
    end_date: datetime
    location: str
    organizer: str
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def validate(self) -> None:
        """
        Valida as regras de negócio da entidade.

        REGRA DE NEGÓCIO:
          A data de início deve ser anterior à data de término.

        Levanta ValueError se as regras forem violadas.
        """
        if self.start_date >= self.end_date:
            raise ValueError(
                "A data de início deve ser anterior à data de término do evento."
            )

        if not self.title.strip():
            raise ValueError("O título do evento não pode estar vazio.")

        if not self.organizer.strip():
            raise ValueError("O organizador do evento não pode estar vazio.")

    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        event_type: Optional[EventType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        location: Optional[str] = None,
        organizer: Optional[str] = None,
    ) -> None:
        """
        Atualiza os campos do evento e registra o horário de atualização.

        Este método encapsula a lógica de atualização dentro da entidade,
        mantendo o controle de quando ela foi modificada (updated_at).
        """
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if event_type is not None:
            self.event_type = event_type
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
        if location is not None:
            self.location = location
        if organizer is not None:
            self.organizer = organizer

        self.updated_at = datetime.utcnow()

        # Revalida após a atualização
        self.validate()
