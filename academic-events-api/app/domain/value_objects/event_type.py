"""
============================================================
VALUE OBJECT: EventType
============================================================

CONCEITO — Value Object (DDD):
  Um Value Object representa um conceito do domínio que é
  definido por seus ATRIBUTOS, não por identidade.
  Dois EventType com o mesmo valor são iguais.

RESPONSABILIDADE:
  Encapsular os tipos válidos de eventos acadêmicos,
  garantindo que apenas valores permitidos sejam usados.

PRINCÍPIO SOLID — OCP (Open/Closed Principle):
  Para adicionar novos tipos, basta adicionar uma nova
  entrada no Enum — sem modificar código existente.

IMPORTANTE:
  Este arquivo não importa nada de FastAPI, SQLModel ou
  qualquer outro framework. É Python puro!
============================================================
"""

from enum import Enum


class EventType(str, Enum):
    """
    Tipos válidos de eventos acadêmicos.

    Herda de `str` para que o valor seja serializado
    como string no JSON (ex: "congress" em vez de "EventType.CONGRESS").
    """

    CONGRESS = "congress"       # Congresso acadêmico
    SEMINAR = "seminar"         # Seminário
    WORKSHOP = "workshop"       # Workshop / Oficina
    LECTURE = "lecture"         # Palestra
    SHORT_COURSE = "short_course"  # Minicurso
    SYMPOSIUM = "symposium"     # Simpósio
    OTHER = "other"             # Outros tipos
