from pydantic import BaseModel
from datetime import datetime

class TrackingBase(BaseModel):
    cargo_id: int
    location: str

class TrackingCreate(TrackingBase):
    pass

class Tracking(TrackingBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True