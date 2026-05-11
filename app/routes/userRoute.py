
from fastapi import APIRouter

router = APIRouter()

# userRepositoy içindeki methodları api haline getireceğiz
from ..repositories import userRepository
from ..schemas import schemas
from ..db import connection


@router.post("/register")
def register(user: schemas.UserCreate):
    db = connection.SessionLocal()
    db_user = userRepository.create_user(db, user)
    db.close()
    return db_user


@router.post("/login")
def login(user: schemas.UserLogin):
    db = connection.SessionLocal()
    user = userRepository.authenticate_user(db, user.email, user.password)
    db.close()
    if user:
        return {"message": "Login successful", "user": user}
    else:
        return {"message": "Invalid email or password"}


