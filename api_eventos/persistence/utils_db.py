from sqlmodel import create_engine

def get_engine():
  url = 'sqlite:///eventos.db'
  engine = create_engine(url)
  return engine