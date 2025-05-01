from pydantic import BaseModel, ConfigDict
from app.schemas.cargo import Cargo


class ContractBase(BaseModel):
    client_name: str
    cargo_type: str
    origin: str
    destination: str
    price: float


class ContractCreate(ContractBase):
    pass


class Contract(ContractBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cargo: "Cargo"
