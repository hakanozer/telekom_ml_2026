# product route dosyasını oluşturuyoruz
from fastapi import APIRouter
from ..repositories import productRepository
from ..schemas import productSchema
from ..db import connection

router = APIRouter()

# product ekleme endpointi oluşturuyoruz
@router.post("/add")
def create_product(product: productSchema.ProductCreate):
    db = connection.SessionLocal()
    db_product = productRepository.create_product(db, product)
    db.close()
    return db_product