from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TrackingBase(BaseModel):
    cargo_id: int
    location: str


class TrackingCreate(TrackingBase):
    pass


class Tracking(TrackingBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    timestamp: datetime
