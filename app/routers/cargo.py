from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, services
from app.db import get_db
from app.logger import logger


router = APIRouter(prefix="/cargoes/")

@router.get("", response_model= list[schemas.Cargo])
def list_cargoes(db: Session = Depends(get_db)):
    logger.info("Listing all cargoes")
    return services.logistics.list_cargoes(db)

@router.get("/cargoes/{cargo_id}", response_model=schemas.Cargo)
def get_cargo(cargo_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching cargo with ID: {cargo_id}")
    cargo_obj = services.logistics.get_cargo(db, cargo_id)
    if not cargo_obj:
        logger.warning(f"Cargo {cargo_id} not found")
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo_obj