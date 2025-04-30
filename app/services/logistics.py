from datetime import datetime

from sqlalchemy.orm import Session

from app import models


def move_vessel(db: Session, vessel_id: int, new_location: str):
    vessel = db.query(models.Vessel).filter_by(id=vessel_id).first()
    if not vessel:
        return None

    # Deliver any in-transit cargo
    for cargo in vessel.cargoes:
        if cargo.status == "in_transit" and cargo.current_location != new_location:
            cargo.current_location = new_location
            if cargo.contract.destination == new_location:
                cargo.status = "delivered"
                cargo.vessel_id = None
            db.add(models.Tracking(
                cargo_id=cargo.id,
                location=new_location,
                timestamp=datetime.now()
            ))

    # Pick up pending cargo at current location if space allows
    available_slots = vessel.capacity - sum(1 for c in vessel.cargoes if c.status == "in_transit")
    if available_slots > 0: # type: ignore
        candidates = db.query(models.Cargo).filter_by(status="pending", current_location=new_location).limit(available_slots).all()
        for cargo in candidates:
            cargo.vessel_id = vessel.id
            cargo.status = "in_transit" # type: ignore
            db.add(models.Tracking(
                cargo_id=cargo.id,
                location=new_location,
                timestamp=datetime.now()
            ))

    vessel.current_location = new_location # type: ignore
    db.commit()
    db.refresh(vessel)
    return vessel

def get_cargo(db: Session, cargo_id: int):
    return db.query(models.Cargo).filter_by(id=cargo_id).first()

def list_cargoes(db: Session):
    return db.query(models.Cargo).all()

def get_tracking_for_cargo(db: Session, cargo_id: int):
    return db.query(models.Tracking).filter_by(cargo_id=cargo_id).order_by(models.Tracking.timestamp).all()