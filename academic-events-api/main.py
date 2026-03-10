"""
============================================================
ARQUIVO PRINCIPAL - Ponto de entrada da aplicação
============================================================

Este arquivo é o ponto de entrada da aplicação FastAPI.
Ele é responsável por:
  1. Criar a instância do FastAPI com metadados
  2. Registrar as rotas (endpoints)
  3. Carregar as configurações do .env
  4. Inicializar o banco de dados (criar tabelas)

ORDEM DE EXECUÇÃO:
  1. Python importa este módulo
  2. FastAPI é instanciado
  3. Lifespan: banco de dados é inicializado
  4. Rotas são registradas
  5. Servidor fica aguardando requisições

COMO RODAR:
  Modo desenvolvimento (com auto-reload):
    uvicorn main:app --reload

  Ou diretamente:
    python main.py

DOCUMENTAÇÃO AUTOMÁTICA (gerada pelo FastAPI):
  Swagger UI: http://localhost:8000/docs
  ReDoc:      http://localhost:8000/redoc
============================================================
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.config.settings import get_settings
from app.infrastructure.database.db import create_db_and_tables
from app.presentation.api.routes.event_routes import router as event_router

# Carrega as configurações do .env
settings = get_settings()


# ------------------------------------------------------------
# Lifespan — Código executado na inicialização e encerramento
# ------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.

    Código ANTES do yield: executado ao INICIAR o servidor
    Código APÓS o yield:   executado ao ENCERRAR o servidor

    NOTA: Esta é a forma moderna do FastAPI para inicialização.
    Substitui os eventos @app.on_event("startup") (deprecated).
    """
    # --- Inicialização ---
    print(f"🚀 Iniciando {settings.app_name} [{settings.app_env}]")
    print(f"📦 Banco de dados: {settings.database_url}")

    # Cria as tabelas no banco (se ainda não existirem)
    # Em produção, use Alembic para migrations (Marco 08)
    create_db_and_tables()

    print("✅ Banco de dados inicializado com sucesso!")

    yield  # Aplicação fica rodando aqui

    # --- Encerramento ---
    print("🔴 Encerrando a aplicação...")


# ------------------------------------------------------------
# Criação da instância principal do FastAPI
# ------------------------------------------------------------
app = FastAPI(
    title=settings.app_name,
    description="""
## Academic Events API

API REST para **Gestão de Eventos Acadêmicos** do IFPI.

### Funcionalidades:
- Cadastro de eventos (congressos, seminários, workshops, etc.)
- Listagem com filtro por período
- Atualização e remoção de eventos

### Arquitetura:
Projeto didático implementando **Clean Architecture + DDD** com FastAPI.
    """,
    version="1.0.0",
    lifespan=lifespan,
)


# ------------------------------------------------------------
# Registro de Rotas
# ------------------------------------------------------------
# Inclui o router de eventos com prefixo /events
# Todos os endpoints ficarão disponíveis em /events/...
app.include_router(event_router)


# ------------------------------------------------------------
# Rota de verificação de saúde (Health Check)
# ------------------------------------------------------------
@app.get("/health", tags=["Health"])
def health_check():
    """
    Verifica se a API está no ar e retorna informações básicas.
    Útil para monitoramento e diagnóstico.
    """
    return {
        "status": "ok",
        "app": settings.app_name,
        "env": settings.app_env,
        "version": "1.0.0",
    }


# ------------------------------------------------------------
# Ponto de entrada para execução direta
# ------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
