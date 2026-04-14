from typing import Annotated

from fastapi import Depends, HTTPException, status

from domain.modelos_autenticacao import UsuarioBasico
from fastapi.security import OAuth2PasswordBearer

from infrastruture import jwt_provider
from persistence.autenticacao_repository import AutenticacaoRepository
from persistence.sqlmodel_autenticacao_repository import SQLModelAutenticacaoRepository
from persistence.utils_db import get_engine


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/signin')

repo = SQLModelAutenticacaoRepository(get_engine())

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

  return UsuarioBasico(id=usuario.id, 
                       email=usuario.email, 
                       nome=usuario.nome)