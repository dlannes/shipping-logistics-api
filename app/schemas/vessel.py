from pydantic import BaseModel, ConfigDict


class VesselBase(BaseModel):
    name: str
    capacity: int
    current_location: str


class VesselCreate(VesselBase):
    pass


class Vessel(VesselBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
