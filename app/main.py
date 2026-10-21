from fastapi import FastAPI
from app.database.connection import Base, engine
from app.routers import auth, tasks

# Cria as tabelas se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API - Modularized",
    version="2.0",
    description="API com Arquitetura Modular e JWT",
)


@app.get("/")
def read_root():
  return {"message": "Bem-vindo à API Segura de Gestão de Tarefas!"}


app.include_router(auth.router)
app.include_router(tasks.router)