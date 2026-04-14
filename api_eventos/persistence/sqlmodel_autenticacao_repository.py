from requests import session

from domain.modelos_autenticacao import Usuario
from sqlmodel import Session, select


class SQLModelAutenticacaoRepository():
  _instance = None

  def __init__(self, engine):
    self.engine = engine

  
  def create(self, email: str, senha: str, nome: str):
    novo_usuario = Usuario(email=email, senha=senha, nome=nome)

    session = Session(self.engine)
    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)
  
    return novo_usuario


  def getByEmail(self, email: str):
    with Session(self.engine) as session:
      instrucao = select(Usuario).where(Usuario.email == email)
      usuario = session.exec(instrucao).first()
      return usuario
  

  def getById(self, id: int):
    with Session(self.engine) as session:
      return session.get(Usuario, id)