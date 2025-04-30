from sqlalchemy.orm import Session

from app import models, schemas


def create_vessel(db: Session, vessel_data: schemas.VesselCreate):
    vessel = models.Vessel(**vessel_data.model_dump())
    db.add(vessel)
    db.commit()
    db.refresh(vessel)
    return vessel

def get_vessel(db: Session, vessel_id: int):
    return db.query(models.Vessel).filter_by(id=vessel_id).first()

def list_vessels(db: Session):
    return db.query(models.Vessel).all()
