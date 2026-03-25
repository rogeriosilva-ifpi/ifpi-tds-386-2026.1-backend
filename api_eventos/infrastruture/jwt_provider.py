import jwt

def generate(payload: dict):
  token = jwt.encode(payload, 'SEGREDO', algorithm='HS256')
  return token


def decode(token: str):
  dados = jwt.decode(token, 'SEGREDO', algorithms=['HS256'])
  return dados