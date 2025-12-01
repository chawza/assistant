from fastapi import FastAPI
from src.api.auth import router as auth_router
from src.api.llm import router as llm_router

app = FastAPI()

app.include_router(auth_router, prefix='/api/auth')
app.include_router(llm_router, prefix='/api/llm')
