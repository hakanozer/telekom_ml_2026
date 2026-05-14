from fastapi import FastAPI

from .routes import userRoute, productRoute, mlRoute

# database işlemleri için connection.py dosyasını import ediyoruz
from .db import connection


# Veritabanı tablolarını oluşturuyoruz
connection.Base.metadata.create_all(bind=connection.engine)

app = FastAPI()

app.include_router(userRoute.router, prefix="/users") 
app.include_router(productRoute.router, prefix="/products")
app.include_router(mlRoute.router, prefix="/ml")