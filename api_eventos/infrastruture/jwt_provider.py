from datetime import datetime, timedelta, timezone
from typing import Literal

import jwt

def generate(payload: dict, tipo: Literal['access', 'refresh']):
  
  expiracao = datetime.now(timezone.utc) + timedelta(seconds=60)

  if tipo == 'refresh':
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=10)

  payload['exp'] = expiracao

  token = jwt.encode(payload, 'SEGREDO', algorithm='HS256')
  return token


def decode(token: str):
  payload = jwt.decode(token, 'SEGREDO', algorithms=['HS256'])
  return payload