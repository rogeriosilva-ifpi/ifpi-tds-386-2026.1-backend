from pydantic import BaseModel


class SignupDTO(BaseModel):
  email: str
  senha: str
  nome: str


class SigninDTO(BaseModel):
  email: str
  senha: str


class RefreshDTO(BaseModel):
  refresh_token: str

