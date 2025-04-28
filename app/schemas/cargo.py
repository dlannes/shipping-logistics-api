
from pydantic import BaseModel, Field
from app.models.tracking import Tracking


class CargoBase(BaseModel):
    contract_id: int
    status: str | None = Field(default="pending")

class CargoCreate(CargoBase):
    pass

class Cargo(CargoBase):
    id: int
    tracking_history: list[Tracking] | None = []

    class Config:
        orm_mode = True
