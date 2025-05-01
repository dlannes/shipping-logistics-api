from sqlalchemy.orm import Session

from app import models


def get_cargo(db: Session, cargo_id: int) -> models.Cargo | None:
    return db.query(models.Cargo).filter_by(id=cargo_id).first()


def list_cargoes(db: Session) -> list[models.Cargo]:
    return db.query(models.Cargo).all()
