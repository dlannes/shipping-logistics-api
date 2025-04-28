from sqlalchemy.orm import Session
from app.models.contract import Contract
from app.schemas.contract import ContractCreate

def create_contract(db: Session, contract: ContractCreate):
    db_contract = Contract(**contract.model_dump())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def get_contract(db: Session, contract_id: int):
    return db.query(Contract).filter(Contract.id == contract_id).first()

def list_contracts(db: Session):
    return db.query(Contract).all()
