"""
============================================================
CONFIGURAÇÕES DA APLICAÇÃO: Settings
============================================================

RESPONSABILIDADE:
  Centralizar TODAS as configurações da aplicação,
  carregando-as a partir de variáveis de ambiente (.env).

TECNOLOGIA:
  Usa pydantic-settings que automaticamente:
    1. Lê o arquivo .env
    2. Valida os tipos dos valores
    3. Fornece valores padrão quando necessário

PRINCÍPIO SOLID — SRP (Single Responsibility):
  Uma única classe responsável por toda configuração.
  O resto da aplicação apenas importa `get_settings()`.

USO:
  from app.infrastructure.config.settings import get_settings

  settings = get_settings()
  print(settings.database_url)
============================================================
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas do arquivo .env.

    Pydantic-settings automaticamente:
      - Busca variáveis de ambiente com os nomes dos campos
      - Faz a conversão de tipos (str -> bool, str -> int, etc.)
      - Lança erro se um campo obrigatório não estiver definido
    """

    # --- Configurações da Aplicação ---
    app_name: str = "Academic Events API"
    app_env: str = "development"
    debug: bool = True

    # --- Banco de Dados ---
    # Valor padrão: SQLite local (sem configuração extra necessária)
    database_url: str = "sqlite:///./academic_events.db"

    # Configuração do pydantic-settings:
    # Diz para ler as variáveis do arquivo ".env"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # DATABASE_URL = database_url
    )

    @property
    def is_sqlite(self) -> bool:
        """Verifica se o banco configurado é SQLite."""
        return self.database_url.startswith("sqlite")

    @property
    def is_production(self) -> bool:
        """Verifica se está em ambiente de produção."""
        return self.app_env == "production"


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna a instância de configurações (singleton via cache).

    O decorador @lru_cache garante que o .env seja lido
    apenas UMA vez durante a vida da aplicação.

    Returns:
        Settings: Instância de configurações
    """
    return Settings()
