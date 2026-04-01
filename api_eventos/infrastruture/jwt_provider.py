import jwt

def generate(payload: dict):
  token = jwt.encode(payload, 'SEGREDO', algorithm='HS256')
  return token


def decode(token: str):
  payload = jwt.decode(token, 'SEGREDO', algorithms=['HS256'])
  return payload