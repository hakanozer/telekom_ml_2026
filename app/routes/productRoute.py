# product route dosyasını oluşturuyoruz
from fastapi import APIRouter, HTTPException
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

# productleri listeleme endpointi oluşturuyoruz
@router.get("/list")
def get_products():
    db = connection.SessionLocal()
    products = productRepository.get_products(db)
    db.close()
    return products

# http://localhost:8000/products/1 gibi bir endpoint oluşturuyoruz
@router.get("/{product_id}")
def get_product(product_id: int):
    db = connection.SessionLocal()
    product = productRepository.get_product(db, product_id)
    db.close()
    # product bulunamazsa 404 hatası döndürüyoruz
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# savea all endpointi oluşturuyoruz
@router.post("/saveall")
def save_all(products: list[productSchema.ProductCreate]):
    db = connection.SessionLocal()
    db_products = productRepository.save_all(db, products)
    db.close()
    return db_products