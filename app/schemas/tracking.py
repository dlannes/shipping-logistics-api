from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Tracking(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cargo_id: int
    location: str
    timestamp: datetime
