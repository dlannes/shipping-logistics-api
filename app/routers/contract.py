from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, services
from app.db import get_db
from app.logger import logger


router = APIRouter(prefix="/contracts")


@router.post("", response_model=schemas.Contract)
def create_contract(
    contract_data: schemas.ContractCreate, db: Session = Depends(get_db)
):
    logger.info(f"Registering new contract for client: {contract_data.client_name}")
    return services.contract.create_contract(db, contract_data)


@router.get("{contract_id}", response_model=schemas.contract.Contract)
def read_contract(contract_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching contract with ID: {contract_id}")
    db_contract = services.contract.get_contract(db, contract_id)
    if not db_contract:
        logger.warning(f"Contract {contract_id} not found")
        raise HTTPException(status_code=404, detail="Contract not found")
    return db_contract


@router.get("", response_model=list[schemas.Contract])
def list_contracts(db: Session = Depends(get_db)):
    logger.info("Listing all contracts")
    return services.contract.list_contracts(db)
