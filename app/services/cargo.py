from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from app import models


class CargoServiceInterface(ABC):
    @abstractmethod
    def get_cargo(self, cargo_id: int) -> Optional[models.Cargo]:
        ...

    @abstractmethod
    def list_cargoes(self) -> list[models.Cargo]:
        ...


class CargoService(CargoServiceInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_cargo(self, cargo_id: int) -> Optional[models.Cargo]:
        return self.db.query(models.Cargo).filter_by(id=cargo_id).first()

    def list_cargoes(self) -> list[models.Cargo]:
        return self.db.query(models.Cargo).all()
