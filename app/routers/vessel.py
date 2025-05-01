from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.services import VesselService
from app.db import get_db
from app.logger import logger


router = APIRouter(prefix="/vessels")

def get_vessel_service(db: Session = Depends(get_db)) -> VesselService:
    return VesselService(db)

@router.post("", response_model=schemas.Vessel)
def create_vessel(vessel_data: schemas.VesselCreate, vessel_service: VesselService = Depends(get_vessel_service)):
    logger.info(f"Registering vessel: {vessel_data.name}")
    return vessel_service.create_vessel(vessel_data)


@router.post("{vessel_id}/move", response_model=schemas.Vessel)
def move_vessel(vessel_id: int, location: str, vessel_service: VesselService = Depends(get_vessel_service)):
    logger.info(f"Moving vessel {vessel_id} to {location}")
    result = vessel_service.move_vessel(vessel_id, location)
    if not result:
        logger.warning(f"Vessel {vessel_id} not found during move")
        raise HTTPException(status_code=404, detail="Vessel not found")
    return result


@router.get("{vessel_id}", response_model=schemas.Vessel)
def get_vessel(vessel_id: int, vessel_service: VesselService = Depends(get_vessel_service)):
    logger.info(f"Fetching vessel with ID: {vessel_id}")
    db_vessel = vessel_service.get_vessel(vessel_id)
    if not db_vessel:
        logger.warning(f"Vessel {vessel_id} not found")
        raise HTTPException(status_code=404, detail="Vessel not found")
    return db_vessel


@router.get("", response_model=list[schemas.Vessel])
def list_vessels(vessel_service: VesselService = Depends(get_vessel_service)):
    logger.info("Listing all vessels")
    return vessel_service.list_vessels()
