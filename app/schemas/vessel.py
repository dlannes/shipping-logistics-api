from pydantic import BaseModel, ConfigDict

from app.schemas.cargo import Cargo


class VesselBase(BaseModel):
    name: str
    capacity: int
    current_location: str


class VesselCreate(VesselBase):
    pass


class Vessel(VesselBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class VesselDetails(Vessel):
    cargoes: list[Cargo]
