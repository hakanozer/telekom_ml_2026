from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

DATABASE_URL = "sqlite:///./project.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

with engine.connect() as conn:
    conn.execute(text("PRAGMA journal_mode=WAL;"))

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()