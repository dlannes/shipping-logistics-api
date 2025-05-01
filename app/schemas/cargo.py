from pydantic import BaseModel, ConfigDict
from app.schemas.tracking import Tracking


class Cargo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    current_location: str | None
    destination: str | None
    vessel_id: int | None


class CargoDetails(Cargo):
    tracking: list[Tracking] = []
