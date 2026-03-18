from fastapi import APIRouter

router = APIRouter()

@router.get('')
def list_inscricoes():
  return 'Lista inscricoes'


@router.post('')
def create_inscricao():
  return 'Confirma Inscricao num evento'


@router.get('/{id}')
def details_inscricao(id:int):
  return f'Detalhes da inscricao {id}'