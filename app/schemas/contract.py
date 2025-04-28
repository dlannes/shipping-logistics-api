from pydantic import BaseModel
from app.models.cargo import Cargo

class ContractBase(BaseModel):
    client_name: str
    cargo_type: str
    destination: str
    price: float

class ContractCreate(ContractBase):
    pass

class Contract(ContractBase):
    id: int
    cargoes: list[Cargo] | None = []

    class Config:
        orm_mode = True
