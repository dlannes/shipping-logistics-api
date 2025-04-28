from sqlalchemy.orm import Session
from app.models.cargo import Cargo
from app.schemas.cargo import CargoCreate


def create_cargo(db: Session, cargo: CargoCreate):
    db_cargo = Cargo(**cargo.model_dump())
    db.add(db_cargo)
    db.commit()
    db.refresh(db_cargo)
    return db_cargo


def get_cargo(db: Session, cargo_id: int):
    return db.query(Cargo).filter(Cargo.id == cargo_id).first()


def list_cargos(db: Session):
    return db.query(Cargo).all()
