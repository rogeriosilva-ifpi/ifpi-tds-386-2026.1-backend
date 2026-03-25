from pwdlib import PasswordHash


pwd_hash = PasswordHash.recommended()

def hash(texto: str):
  return pwd_hash.hash(texto)


def verify_hash(texto: str, hash: str):
  return pwd_hash.verify(texto, hash)