# user model için repository dosyasını oluşturuyoruz - register ve login işlemlerini burada yapacağız
from sqlalchemy.orm import Session
from ..schemas import schemas
from ..db import connection
from ..models import models

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()