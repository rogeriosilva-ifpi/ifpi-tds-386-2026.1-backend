from fastapi import APIRouter, status, HTTPException

from domain.modelos_autenticacao import UsuarioBasico
from persistence.autenticacao_repository import AutenticacaoRepository
from presentation.dtos.autenticacao_dtos import SigninDTO, SignupDTO
from infrastruture import hash_provider, jwt_provider

router = APIRouter()
repo = AutenticacaoRepository()


@router.post('/signup',
             response_model=UsuarioBasico, 
             status_code=status.HTTP_201_CREATED)
def signup(dados: SignupDTO):
  hash = hash_provider.hash(dados.senha)
  usuario = repo.create(email=dados.email, 
                        senha=hash, 
                        nome=dados.nome)
  return usuario


@router.post('/signin')
def signin(dados: SigninDTO):
  usuario_encontrado = repo.getByEmail(email=dados.email)

  if not usuario_encontrado:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Usuário não localizado')

  if not hash_provider.verify_hash(dados.senha, usuario_encontrado.senha):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Senha incorreta')

  access_token = jwt_provider.generate({'sub': usuario_encontrado.id})
  return {'access_token': access_token}


@router.get('/me')
def me():
  # TODO
  ..