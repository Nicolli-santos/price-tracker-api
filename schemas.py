from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

# Esquema base com campos comuns de um produto
class ProductBase(BaseModel):
    name: str
    url: str
    target_price: float

# Esquema usado para CRIAR um produto (o que o usuário envia na requisição)
class ProductCreate(ProductBase):
    pass

# Esquema usado para EXIBIR o histórico de preços
class PriceHistoryResponse(BaseModel):
    id: int
    price: float
    timestamp: datetime

    class Config:
        from_attributes = True

# Esquema completo usado para RETORNAR um produto da API
class ProductResponse(ProductBase):
    id: int
    current_price: Optional[float] = None
    prices: List[PriceHistoryResponse] = []

    class Config:
        from_attributes = True
        