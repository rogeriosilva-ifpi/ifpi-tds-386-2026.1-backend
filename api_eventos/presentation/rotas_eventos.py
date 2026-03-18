from fastapi import APIRouter, status
from domain.modelos import Evento
from persistence.eventos_repository import EventoRepository

router = APIRouter()

repo_eventos = EventoRepository()

@router.get('', 
         response_model=list[Evento])
def list_eventos():
  return repo_eventos.all()


@router.post('', 
          status_code=status.HTTP_201_CREATED, 
          response_model=Evento)
def create_evento(novo_evento: Evento):
  return repo_eventos.create(novo_evento)
