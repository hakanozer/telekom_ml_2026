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

# productleri listelemek için bir fonksiyon oluşturuyoruz
def get_products(db: Session):
    return db.query(models.Product).all()

# id değerinine göre product getirmek için bir fonksiyon oluşturuyoruz
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

# product save all işlemi için bir fonksiyon oluşturuyoruz
def save_all(db: Session, products: list[productSchema.ProductCreate]):
    db_products = []
    for product in products:
        db_product = models.Product(title=product.title, description=product.description, price=product.price)
        db.add(db_product)
        db_products.append(db_product)
    db.commit()
    for db_product in db_products:
        db.refresh(db_product)
    return db_products

# product silme işlemi için bir fonksiyon oluşturuyoruz
def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

# product güncelleme işlemi için bir fonksiyon oluşturuyoruz
def update_product(db: Session, product_id: int, product: productSchema.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.title = product.title
        db_product.description = product.description
        db_product.price = product.price
        db.commit()
        db.refresh(db_product)
        return db_product
    return None