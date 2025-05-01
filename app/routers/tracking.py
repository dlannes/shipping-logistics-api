from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import cast

from app.schemas import Tracking
from app.services import TrackingService
from app.db import get_db
from app.logger import logger


router = APIRouter(prefix="/trackings", tags=["Tracking"])


def get_tracking_service(db: Session = Depends(get_db)) -> TrackingService:
    return TrackingService(db)


@router.get("/{cargo_id}")
def get_tracking_for_cargo(
    cargo_id: int, tracking_service: TrackingService = Depends(get_tracking_service)
) -> list[Tracking]:
    logger.info(f"Fetching tracking for cargo ID: {cargo_id}")
    tracking_info = tracking_service.get_tracking_for_cargo(cargo_id)
    if not tracking_info:
        logger.warning(f"Tracking information for cargo {cargo_id} not found")
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cast(list, tracking_info)
