from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from domain.modelos_autenticacao import Usuario, UsuarioBasico
from persistence.autenticacao_repository import AutenticacaoRepository
from presentation.dtos.autenticacao_dtos import RefreshDTO, SigninDTO, SignupDTO
from infrastruture import hash_provider, jwt_provider
from presentation.utils.auth_utils import get_current_user

router = APIRouter()
repo = AutenticacaoRepository.getInstance()

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

  access_token = jwt_provider.generate({'sub': usuario_encontrado.email}, 'access')
  refresh_token = jwt_provider.generate({'sub': usuario_encontrado.email}, 'refresh')
  return {'access_token': access_token,
          'refresh_token': refresh_token}


@router.get('/me')
def me(user: Annotated[Usuario, Depends(get_current_user)]):
  return user


@router.post('/refresh')
def refresh(dados: RefreshDTO):
  refresh_token = dados.refresh_token

  try:
    payload = jwt_provider.decode(refresh_token)
  except:
    raise HTTPException(status_code=400, detail='Refresh Token inválido!')
  
  email = payload.get('sub')
  usuario = repo.getByEmail(email)

  if not usuario:
    raise HTTPException(status_code=400, detail='Refresh Token inválido(email não localizado)!')

  access_token = jwt_provider.generate({'sub': usuario.email}, 'access')
  refresh_token = jwt_provider.generate({'sub': usuario.email}, 'refresh')
  return {'access_token': access_token,
          'refresh_token': refresh_token}