from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from persistence.utils_db import get_engine
from presentation.rotas_autenticacao import router as auth_router
from presentation.rotas_eventos import router as eventos_router
from presentation.rotas_inscricoes import router as inscricoes_router

# Application
app = FastAPI()

# SQL Model 

# Criar as tabelas no Banco de Dados
SQLModel.metadata.create_all(get_engine())

# Controllers / Rotas
app.include_router(auth_router, prefix='/auth')
app.include_router(eventos_router, prefix='/events')
app.include_router(inscricoes_router, prefix='/enrollments')



