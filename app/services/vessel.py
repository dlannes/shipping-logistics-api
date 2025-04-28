from sqlalchemy.orm import Session
from app.models.vessel import Vessel
from app.schemas.vessel import VesselCreate

def create_vessel(db: Session, vessel: VesselCreate):
    db_vessel = Vessel(**vessel.model_dump())
    db.add(db_vessel)
    db.commit()
    db.refresh(db_vessel)
    return db_vessel

def get_vessel(db: Session, vessel_id: int):
    return db.query(Vessel).filter(Vessel.id == vessel_id).first()

def list_vessels(db: Session):
    return db.query(Vessel).all()
