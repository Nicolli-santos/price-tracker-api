from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import scraper
from database import engine, get_db

# Cria as tabelas no banco de dados automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Price Tracker API")


@app.get("/")
def read_root():
    return {"message": "Price Tracker API running smoothly!"}


# Rota 1: Cadastrar um novo produto
@app.post(
    "/products",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = (
        db.query(models.Product)
        .filter(models.Product.url == str(product.url))
        .first()
    )
    if db_product:
        raise HTTPException(
            status_code=400, detail="Product with this URL is already registered."
        )

    new_product = models.Product(
        name=product.name, url=str(product.url), target_price=product.target_price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Rota 2: Listar todos os produtos
@app.get("/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


# Rota 3: Rodar o scraper e atualizar o preço do produto
@app.post("/products/{product_id}/check-price", response_model=schemas.ProductResponse)
def check_product_price(product_id: int, db: Session = Depends(get_db)):
    # 1. Busca o produto no banco
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 2. Executa o scraper na URL do produto
    new_price = scraper.fetch_product_price(product.url)
    if new_price is None:
        raise HTTPException(
            status_code=500, detail="Could not extract price from the provided URL"
        )

    # 3. Atualiza o preço atual do produto
    product.current_price = new_price

    # 4. Registra o histórico de preço
    price_entry = models.PriceHistory(product_id=product.id, price=new_price)
    db.add(price_entry)

    db.commit()
    db.refresh(product)
    return product