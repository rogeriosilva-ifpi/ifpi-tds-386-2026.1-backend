from fastapi import FastAPI
from presentation.rotas_autenticacao import router as auth_router
from presentation.rotas_eventos import router as eventos_router
from presentation.rotas_inscricoes import router as inscricoes_router

# Application
app = FastAPI()

# Controllers / Rotas
app.include_router(auth_router, prefix='/auth')
app.include_router(eventos_router, prefix='/events')
app.include_router(inscricoes_router, prefix='/enrollments')



