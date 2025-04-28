from sqlalchemy.orm import Session
from app.models.tracking import Tracking
from app.schemas.tracking import TrackingCreate

def create_tracking(db: Session, tracking: TrackingCreate):
    db_tracking = Tracking(**tracking.dict())
    db.add(db_tracking)
    db.commit()
    db.refresh(db_tracking)
    return db_tracking

def get_tracking(db: Session, tracking_id: int):
    return db.query(Tracking).filter(Tracking.id == tracking_id).first()

def list_trackings(db: Session):
    return db.query(Tracking).all()
