from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import userRoute, productRoute, mlRoute

# database işlemleri için connection.py dosyasını import ediyoruz
from .db import connection

# Veritabanı tablolarını oluşturuyoruz
connection.Base.metadata.create_all(bind=connection.engine)

app = FastAPI()

# add cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm originlere izin ver
    allow_methods=["*"],  # Tüm HTTP metodlarına izin ver
    allow_headers=["*"],  # Tüm header'lara izin ver
)

app.include_router(userRoute.router, prefix="/users") 
app.include_router(productRoute.router, prefix="/products")
app.include_router(mlRoute.router, prefix="/ml")