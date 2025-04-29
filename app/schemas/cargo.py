from pydantic import BaseModel, Field, ConfigDict
from app.schemas.tracking import Tracking

class CargoBase(BaseModel):
    contract_id: int
    status: str | None = Field(default="pending")


class CargoCreate(CargoBase):
    pass


class Cargo(CargoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tracking_history: list["Tracking"] | None = []