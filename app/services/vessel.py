from abc import ABC, abstractmethod
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas


#TODO: check types

class VesselServiceInterface(ABC):
    @abstractmethod
    def create_vessel(self, vessel_data: schemas.VesselCreate) -> models.Vessel:
        ...

    @abstractmethod
    def get_vessel(self, vessel_id: int) -> Optional[models.Vessel]:
        ...

    @abstractmethod
    def list_vessels(self) -> List[models.Vessel]:
        ...

    @abstractmethod
    def move_vessel(
        self, vessel_id: int, new_location: str
    ) -> Optional[models.Vessel]:
        ...


class VesselService(VesselServiceInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_vessel(self, vessel_data: schemas.VesselCreate) -> models.Vessel:
        vessel = models.Vessel(**vessel_data.model_dump())
        self.db.add(vessel)
        self.db.commit()
        self.db.refresh(vessel)
        return vessel

    def get_vessel(self, vessel_id: int) -> Optional[models.Vessel]:
        return self.db.query(models.Vessel).filter_by(id=vessel_id).first()

    def list_vessels(self) -> List[models.Vessel]:
        return self.db.query(models.Vessel).all()

    def move_vessel(
        self, vessel_id: int, new_location: str
    ) -> Optional[models.Vessel]:
        vessel = self.db.query(models.Vessel).filter_by(id=vessel_id).first()
        if not vessel:
            return None

        # Deliver any in-transit cargo
        for cargo in vessel.cargoes:
            if cargo.status == "in_transit" and cargo.current_location != new_location:
                cargo.current_location = new_location
                if cargo.contract.destination == new_location:
                    cargo.status = "delivered"
                    cargo.vessel_id = None
                self.db.add(
                    models.Tracking(
                        cargo_id=cargo.id, location=new_location, timestamp=datetime.now()
                    )
                )

        # Pick up pending cargo at current location if space allows
        available_slots = vessel.capacity - sum(
            1 for c in vessel.cargoes if c.status == "in_transit"
        )
        if available_slots > 0: # type: ignore
            candidates = (
                self.db.query(models.Cargo)
                .filter_by(status="pending", current_location=new_location)
                .limit(available_slots)
                .all()
            )
            for cargo in candidates:
                cargo.vessel_id = vessel.id
                cargo.status = "in_transit" # type: ignore
                self.db.add(
                    models.Tracking(
                        cargo_id=cargo.id, location=new_location, timestamp=datetime.now()
                    )
                )

        vessel.current_location = new_location # type: ignore
        self.db.commit()
        self.db.refresh(vessel)
        return vessel
