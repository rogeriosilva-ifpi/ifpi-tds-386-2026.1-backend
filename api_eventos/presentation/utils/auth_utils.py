from re import S
from typing import Annotated

from fastapi import Depends, HTTPException, status

from domain.modelos_autenticacao import UsuarioBasico
from persistence.autenticacao_repository import AutenticacaoRepository
from fastapi.security import OAuth2PasswordBearer

from infrastruture import jwt_provider


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/signin')

repo = AutenticacaoRepository()


def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
  # 1. Investigar a Request para token
  # 2. Extrair o email de dentro do token
  # 3. Buscar o usuário pelo email no repositório
  # 4. Retornar o usuário
  try:
    payload = jwt_provider.decode(token)
    email = payload.get('sub')
  except:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Token Inválido')
  

  usuario = repo.getByEmail(email)
  print('Email', email)
  print('Usuario', usuario)

  
  return UsuarioBasico(id=usuario.id, 
                       email=usuario.email, 
                       nome=usuario.nome)