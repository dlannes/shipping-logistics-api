from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, services
from app.db import get_db
from app.logger import logger


router = APIRouter(prefix="/trackings")


# TODO: not found


@router.get("{cargo_id}", response_model=list[schemas.Tracking])
def get_tracking_for_cargo(cargo_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching tracking for cargo ID: {cargo_id}")
    return services.tracking.get_tracking_for_cargo(db, cargo_id)
