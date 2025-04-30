from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, services
from app.db import get_db
from app.logger import logger


router = APIRouter(prefix="/vessels/")


@router.post("", response_model=schemas.Vessel)
def create_vessel(vessel_data: schemas.VesselCreate, db: Session = Depends(get_db)):
    logger.info(f"Registering vessel: {vessel_data.name}")
    return services.vessel.create_vessel(db, vessel_data)

@router.post("/vessels/{vessel_id}/move", response_model=schemas.Vessel)
def move_vessel(vessel_id: int, location: str, db: Session = Depends(get_db)):
    logger.info(f"Moving vessel {vessel_id} to {location}")
    result = services.logistics.move_vessel(db, vessel_id, location)
    if not result:
        logger.warning(f"Vessel {vessel_id} not found during move")
        raise HTTPException(status_code=404, detail="Vessel not found")
    return result

@router.get("/vessels/{vessel_id}", response_model=schemas.Vessel)
def get_vessel(vessel_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching vessel with ID: {vessel_id}")
    db_vessel = services.vessel.get_vessel(db, vessel_id)
    if not db_vessel:
        logger.warning(f"Vessel {vessel_id} not found")
        raise HTTPException(status_code=404, detail="Vessel not found")
    return db_vessel

@router.get("/vessels/", response_model=list[schemas.Vessel])
def list_vessels(db: Session = Depends(get_db)):
    logger.info("Listing all vessels")
    return services.vessel.list_vessels(db)