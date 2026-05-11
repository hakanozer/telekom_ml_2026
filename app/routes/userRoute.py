# bu py dosyasını farstapi route'larını tanımlamak için kullanacağız
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def get_users():
    return {"users": ["Alice", "Bob", "Charlie"]}