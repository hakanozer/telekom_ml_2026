# user model için repository dosyasını oluşturuyoruz - register ve login işlemlerini burada yapacağız
from sqlalchemy.orm import Session
from ..schemas import schemas
from ..db import connection
from ..models import models

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(db_user) # insert into users (name, email, password) values (user.name, user.email, user.password)
    db.commit()
    db.refresh(db_user)
    return db_user


# email ve password ile kullanıcıyı doğrulamak için bir fonksiyon oluşturuyoruz
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and user.password == password:
        return user
    return None