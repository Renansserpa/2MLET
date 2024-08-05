from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.endpoints import scrap_api
from app.api.endpoints import data_api
from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup (executado ao iniciar a aplicação)
    init_db()
    yield
    # Cleanup (executado ao desligar a aplicação)
    pass

app = FastAPI(lifespan=lifespan)

app.include_router(scrap_api.router, prefix='/scrap', tags=['scrap'])
app.include_router(data_api.router)