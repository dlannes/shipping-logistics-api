from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session

from app import models, schemas


class ContractServiceInterface(ABC):
    @abstractmethod
    def create_contract(
        self, contract_data: schemas.ContractCreate
    ) -> models.Contract: ...

    @abstractmethod
    def get_contract(self, contract_id: int) -> Optional[models.Contract]: ...

    @abstractmethod
    def list_contracts(self) -> list[models.Contract]: ...


class ContractService(ContractServiceInterface):
    def __init__(self, db: Session):
        self.db = db

    def create_contract(self, contract_data: schemas.ContractCreate) -> models.Contract:
        contract = models.Contract(**contract_data.model_dump())
        self.db.add(contract)
        self.db.flush()

        cargo = models.Cargo(
            contract_id=contract.id,
            status="pending",
            current_location=contract.origin,
        )
        self.db.add(cargo)
        self.db.commit()
        self.db.refresh(contract)
        return contract

    def get_contract(self, contract_id: int) -> Optional[models.Contract]:
        return self.db.query(models.Contract).filter_by(id=contract_id).first()

    def list_contracts(self) -> list[models.Contract]:
        return self.db.query(models.Contract).all()
