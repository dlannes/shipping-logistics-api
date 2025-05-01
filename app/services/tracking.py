from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session

from app import models


class TrackingServiceInterface(ABC):
    @abstractmethod
    def get_tracking_for_cargo(self, cargo_id: int) -> List[models.Tracking]: ...


class TrackingService(TrackingServiceInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_tracking_for_cargo(self, cargo_id: int) -> List[models.Tracking]:
        return (
            self.db.query(models.Tracking)
            .filter_by(cargo_id=cargo_id)
            .order_by(models.Tracking.timestamp)
            .all()
        )
