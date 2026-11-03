from contextlib import asynccontextmanager
from fastapi import FastAPI

from .routers import router
from .services import load_model

@asynccontextmanager
async def lifespan(app:FastAPI):
    #Executa na inicialização
    load_model()

    yield


app = FastAPI(
    title= 'Que número é esse AI?',
    lifespan=lifespan
    )

app.include_router(router)