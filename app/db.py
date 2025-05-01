from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./alembic.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session | None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
