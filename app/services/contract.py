from sqlalchemy.orm import Session

from app import models, schemas


def create_contract(db: Session, contract_data: schemas.ContractCreate):
    contract = models.Contract(**contract_data.model_dump())
    db.add(contract)
    db.flush()

    cargo = models.Cargo(
        contract_id=contract.id,
        status="pending",
        current_location=contract.origin
    )
    db.add(cargo)
    db.commit()
    db.refresh(contract)
    return contract

def get_contract(db: Session, contract_id: int):
    return db.query(models.Contract).filter_by(id=contract_id).first()

def list_contracts(db: Session):
    return db.query(models.Contract).all()
