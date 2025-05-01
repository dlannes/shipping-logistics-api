from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import cast

from app.schemas import Cargo
from app.services import CargoService
from app.db import get_db
from app.logger import logger


router = APIRouter(prefix="/cargoes", tags=["Cargo"])


def get_cargo_service(db: Session = Depends(get_db)) -> CargoService:
    return CargoService(db)


@router.get("")
def list_cargoes(
    cargo_service: CargoService = Depends(get_cargo_service),
) -> list[Cargo]:
    logger.info("Listing all cargoes")
    return cast(list, cargo_service.list_cargoes())


@router.get("/{cargo_id}")
def get_cargo(
    cargo_id: int, cargo_service: CargoService = Depends(get_cargo_service)
) -> Cargo:
    logger.info(f"Fetching cargo with ID: {cargo_id}")
    cargo_obj = cargo_service.get_cargo(cargo_id)
    if not cargo_obj:
        logger.warning(f"Cargo {cargo_id} not found")
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo_obj
