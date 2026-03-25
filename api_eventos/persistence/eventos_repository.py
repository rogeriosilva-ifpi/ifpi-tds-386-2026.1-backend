from domain.modelos_eventos import Evento


class EventoRepository():
  # Conversa com BD
  
  def __init__(self):
    self.eventos = [
        Evento(id=1, 
              nome='CasaCor 2026', 
              data_inicio='01/04/2026', 
              data_fim='30/06/2026',
              endereco='Av. Pres. Kennedy'),
        Evento(id=2,
              nome='Maratona de Programação 2026',
              data_inicio='17/09/2026',
              data_fim='16/09/2026',
              endereco='UFPI - Teresina')
      ]

  def all(self):
    return self.eventos
  
  def create(self, novo: Evento):
    self.eventos.append(novo)
    return novo