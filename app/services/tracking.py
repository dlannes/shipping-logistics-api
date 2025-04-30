from sqlalchemy.orm import Session

from app import models


def get_tracking_for_cargo(db: Session, cargo_id: int):
    return db.query(models.Tracking).filter_by(cargo_id=cargo_id).order_by(models.Tracking.timestamp).all()