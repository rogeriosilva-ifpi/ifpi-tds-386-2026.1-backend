"""
============================================================
ARQUIVO PRINCIPAL - Ponto de entrada da aplicação
============================================================

Este arquivo é o ponto de entrada da aplicação FastAPI.
Ele é responsável por:
  1. Criar a instância do FastAPI
  2. Registrar as rotas (endpoints)
  3. Carregar as configurações
  4. Inicializar a infraestrutura (banco de dados)

NOTA DIDÁTICA:
  Este arquivo será incrementado a cada marco do projeto.
  No Marco 01, ele contém apenas o esqueleto inicial.
============================================================
"""

from fastapi import FastAPI

# Criação da instância principal do FastAPI
# O título e versão aparecem na documentação automática (/docs)
app = FastAPI(
    title="Academic Events API",
    description="API de Gestão de Eventos Acadêmicos - Projeto Didático de Clean Architecture + DDD",
    version="0.1.0",
)


# ------------------------------------------------------------
# Rota de verificação de saúde (Health Check)
# ------------------------------------------------------------
@app.get("/health", tags=["Health"])
def health_check():
    """
    Verifica se a API está no ar.
    Útil para monitoramento e diagnóstico.
    """
    return {"status": "ok", "message": "Academic Events API está rodando!"}


# ------------------------------------------------------------
# Ponto de entrada para execução direta
# ------------------------------------------------------------
# Para rodar: python main.py  OU  uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
