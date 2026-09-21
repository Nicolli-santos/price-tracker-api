from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# Cria as tabelas no banco de dados automaticamente se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Price Tracker API")


@app.get("/")
def read_root():
    return {"message": "Price Tracker API with Database is running!"}