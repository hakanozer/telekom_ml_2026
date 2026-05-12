# productreposiyory için repository dosyasını oluşturuyoruz - create
from sqlalchemy.orm import Session
from ..schemas import productSchema
from ..db import connection
from ..models import models

# product oluşturmak için bir fonksiyon oluşturuyoruz
def create_product(db: Session, product: productSchema.ProductCreate):
    db_product = models.Product(title=product.title, description=product.description, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product