"""
============================================================
CONFIGURAÇÃO DO ALEMBIC: env.py
============================================================

RESPONSABILIDADE:
  Configurar o Alembic para usar:
    1. A DATABASE_URL do nosso sistema de configurações (.env)
    2. O metadata do SQLModel para autogenerate de migrations

COMO FUNCIONA:
  O Alembic usa este arquivo para:
    - Conectar ao banco de dados
    - Comparar o estado atual das tabelas com os models
    - Gerar automaticamente o SQL de migração

AUTOGENERATE:
  Com `target_metadata = SQLModel.metadata`, o Alembic
  consegue detectar mudanças nos models e gerar as
  migrations automaticamente com:
    alembic revision --autogenerate -m "descrição"
============================================================
"""

import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlmodel import SQLModel

from alembic import context

# Adiciona o diretório raiz do projeto ao Python path
# para que os imports dos models funcionem corretamente
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa os models para que o SQLModel.metadata os conheça
# IMPORTANTE: todos os models devem ser importados aqui!
from app.infrastructure.database.models.event_model import EventModel  # noqa: F401
from app.infrastructure.config.settings import get_settings

# Objeto de configuração do Alembic
config = context.config

# Configura logging do Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ----------------------------------------------------------
# PONTO CHAVE: Conecta o Alembic ao nosso sistema de settings
# ----------------------------------------------------------
settings = get_settings()

# Substitui a URL do alembic.ini pela nossa DATABASE_URL do .env
config.set_main_option("sqlalchemy.url", settings.database_url)

# Fornece o metadata do SQLModel para o autogenerate
# O Alembic comparará este metadata com o banco para gerar migrations
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """
    Executa migrations em modo 'offline' (sem conexão ativa).

    Gera o SQL sem precisar de uma conexão com o banco.
    Útil para revisar o SQL antes de executar.

    Comando: alembic upgrade head --sql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Executa migrations em modo 'online' (com conexão ativa).

    Conecta ao banco e executa as migrations diretamente.

    Comando: alembic upgrade head
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
