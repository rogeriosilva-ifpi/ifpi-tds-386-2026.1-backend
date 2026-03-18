from fastapi import APIRouter

router = APIRouter()

@router.post('/signup')
def signup():
  return 'Registra-se na plataforma de eventos'


@router.post('/signin')
def signin():
  return 'Autentica-se na plataforma'


@router.get('/me')
def me():
  return 'Retornar o Perfil do usuário logado'