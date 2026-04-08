from domain.modelos_autenticacao import Usuario


class AutenticacaoRepository():
  _instance = None

  def __init__(self):
    self.usuarios:list[Usuario] = []
    self.proximo_id = 1

  
  # Design Pattern Singleton
  @classmethod
  def getInstance(cls):
    if not cls._instance:
      cls._instance = AutenticacaoRepository()
    
    return cls._instance


  
  def create(self, email: str, senha: str, nome: str):
    novo_usuario = Usuario(id=self.proximo_id, email=email, senha=senha, nome=nome)
    self.usuarios.append(novo_usuario)
    self.proximo_id += 1

    return novo_usuario


  def getByEmail(self, email: str):
    for usuario in self.usuarios:
      if usuario.email == email:
        return usuario
    
    return None
  

  def getById(self, id: int):
    for usuario in self.usuarios:
      if usuario.id == id:
        return usuario
    
    return None