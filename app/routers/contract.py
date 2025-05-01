from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.services import ContractService
from app.db import get_db
from app.logger import logger


router = APIRouter(prefix="/contracts")


def get_contract_service(db: Session = Depends(get_db)) -> ContractService:
    return ContractService(db)


@router.post("", response_model=schemas.Contract)
def create_contract(
    contract_data: schemas.ContractCreate,
    contract_service: ContractService = Depends(get_contract_service)
):
    logger.info(f"Registering new contract for client: {contract_data.client_name}")
    return contract_service.create_contract ( contract_data)


@router.get("/{contract_id}", response_model=schemas.contract.Contract)
def read_contract(contract_id: int, contract_service: ContractService = Depends(get_contract_service)):
    logger.info(f"Fetching contract with ID: {contract_id}")
    db_contract = contract_service.get_contract(contract_id)
    if not db_contract:
        logger.warning(f"Contract {contract_id} not found")
        raise HTTPException(status_code=404, detail="Contract not found")
    return db_contract


@router.get("", response_model=list[schemas.Contract])
def list_contracts(contract_service: ContractService = Depends(get_contract_service)):
    logger.info("Listing all contracts")
    return contract_service.list_contracts()
