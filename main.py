from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

# Cria as tabelas no banco de dados automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Price Tracker API")


@app.get("/")
def read_root():
    return {"message": "Price Tracker API running smoothly!"}


# Rota 1: Cadastrar um novo produto no banco
@app.post(
    "/products",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # Verifica se a URL já está cadastrada
    db_product = (
        db.query(models.Product)
        .filter(models.Product.url == str(product.url))
        .first()
    )
    if db_product:
        raise HTTPException(
            status_code=400, detail="Product with this URL is already registered."
        )

    # Cria o produto no banco
    new_product = models.Product(
        name=product.name, url=str(product.url), target_price=product.target_price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Rota 2: Listar todos os produtos cadastrados
@app.get("/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products