from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import cast

from app.schemas import Tracking
from app.services import TrackingService
from app.db import get_db
from app.logger import logger


router = APIRouter(prefix="/trackings", tags=["Tracking"])


# TODO: not found
def get_tracking_service(db: Session = Depends(get_db)) -> TrackingService:
    return TrackingService(db)


@router.get("/{cargo_id}")
def get_tracking_for_cargo(
    cargo_id: int, tracking_service: TrackingService = Depends(get_tracking_service)
) -> list[Tracking]:
    logger.info(f"Fetching tracking for cargo ID: {cargo_id}")
    return cast(list, tracking_service.get_tracking_for_cargo(cargo_id))
