from pydantic import BaseModel
from app.schemas.cargo import Cargo


class ContractBase(BaseModel):
    client_name: str
    cargo_type: str
    destination: str
    price: float


class ContractCreate(ContractBase):
    pass


class Contract(ContractBase):
    id: int
    cargos: list["Cargo"] | None = []

    class Config:
        from_attributes = True
