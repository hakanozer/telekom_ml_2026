# productSchema oluşturuyoruz
from pydantic import BaseModel

class ProductSchema(BaseModel):
    id: int
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True
        
        
# product oluşturmak için bir schema daha oluşturuyoruz
class ProductCreate(BaseModel):
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True