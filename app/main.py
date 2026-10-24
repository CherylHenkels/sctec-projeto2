from fastapi import FastAPI
from .routers import router

app = FastAPI(title= 'Que número é esse AI?')
app.include_router(router)