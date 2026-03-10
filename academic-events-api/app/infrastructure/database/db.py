"""
============================================================
CONFIGURAÇÃO DO BANCO DE DADOS: db.py
============================================================

RESPONSABILIDADE:
  Criar e gerenciar a conexão com o banco de dados usando SQLModel.
  Fornece:
    - Engine (conexão com o banco)
    - SessionLocal (fábrica de sessões)
    - Função para criar as tabelas

TECNOLOGIA: SQLModel
  SQLModel combina SQLAlchemy (para persistência) com
  Pydantic (para validação), eliminando código duplicado.

CONCEITO — Session:
  Uma Session representa uma "conversa" com o banco de dados.
  Cada requisição HTTP deve usar sua própria session,
  que é aberta no início e fechada ao final da requisição.

  Isso é gerenciado pelo FastAPI via Dependency Injection
  (ver shared/dependencies.py).
============================================================
"""

from typing import Generator

from sqlmodel import SQLModel, Session, create_engine

from app.infrastructure.config.settings import get_settings

# Obtém as configurações (DATABASE_URL do .env)
settings = get_settings()

# ------------------------------------------------------------
# Configuração especial para SQLite
# ------------------------------------------------------------
# O SQLite não suporta múltiplas threads por padrão.
# Para uso com FastAPI (que é assíncrono), precisamos
# desabilitar essa verificação com connect_args.
connect_args = {}
if settings.is_sqlite:
    connect_args = {"check_same_thread": False}

# ------------------------------------------------------------
# Engine — Conexão principal com o banco de dados
# ------------------------------------------------------------
# O engine é criado UMA VEZ e reutilizado por toda a aplicação.
# É o objeto responsável por gerenciar o pool de conexões.
engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=settings.debug,  # Se True, imprime o SQL gerado no console
)


def create_db_and_tables() -> None:
    """
    Cria todas as tabelas no banco de dados.

    Deve ser chamado na inicialização da aplicação (main.py).
    O SQLModel usa os modelos definidos em infrastructure/database/models/
    para criar as tabelas automaticamente.

    NOTA: Em produção, use Alembic para migrations (Marco 08).
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Gerador de sessões do banco de dados.

    Usado como dependência do FastAPI (Dependency Injection).
    Garante que a sessão seja SEMPRE fechada após a requisição,
    mesmo em caso de erro (bloco finally).

    Exemplo de uso no endpoint:
        @app.get("/events")
        def list_events(session: Session = Depends(get_session)):
            ...
    """
    with Session(engine) as session:
        yield session
        # O `with` garante o fechamento automático da sessão
