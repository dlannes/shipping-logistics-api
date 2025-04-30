from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, services
from app.db import get_db
from app.logger import logger


app = FastAPI(title="Shipping Logistics API", version="1.0")


# --- Contracts ---

@app.post("/contracts/", response_model=schemas.contract.Contract)
def create_contract(contract_data: schemas.contract.ContractCreate, db: Session = Depends(get_db)):
    logger.info(f"Registering new contract for client: {contract_data.client_name}")
    return services.contract.create_contract(db, contract_data)

@app.get("/contracts/{contract_id}", response_model=schemas.contract.Contract)
def read_contract(contract_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching contract with ID: {contract_id}")
    db_contract = services.contract.get_contract(db, contract_id)
    if not db_contract:
        logger.warning(f"Contract {contract_id} not found")
        raise HTTPException(status_code=404, detail="Contract not found")
    return db_contract

@app.get("/contracts/", response_model=List[schemas.contract.Contract])
def list_contracts(db: Session = Depends(get_db)):
    logger.info("Listing all contracts")
    return services.contract.list_contracts(db)


# --- Vessels ---

@app.post("/vessels/", response_model=schemas.vessel.Vessel)
def create_vessel(vessel_data: schemas.vessel.VesselCreate, db: Session = Depends(get_db)):
    logger.info(f"Registering vessel: {vessel_data.name}")
    return services.vessel.create_vessel(db, vessel_data)

@app.post("/vessels/{vessel_id}/move", response_model=schemas.vessel.Vessel)
def move_vessel(vessel_id: int, location: str, db: Session = Depends(get_db)):
    logger.info(f"Moving vessel {vessel_id} to {location}")
    result = services.logistics.move_vessel(db, vessel_id, location)
    if not result:
        logger.warning(f"Vessel {vessel_id} not found during move")
        raise HTTPException(status_code=404, detail="Vessel not found")
    return result

@app.get("/vessels/{vessel_id}", response_model=schemas.vessel.Vessel)
def get_vessel(vessel_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching vessel with ID: {vessel_id}")
    db_vessel = services.vessel.get_vessel(db, vessel_id)
    if not db_vessel:
        logger.warning(f"Vessel {vessel_id} not found")
        raise HTTPException(status_code=404, detail="Vessel not found")
    return db_vessel

@app.get("/vessels/", response_model=List[schemas.vessel.Vessel])
def list_vessels(db: Session = Depends(get_db)):
    logger.info("Listing all vessels")
    return services.vessel.list_vessels(db)


# --- Cargoes ---

@app.get("/cargoes/", response_model=List[schemas.cargo.Cargo])
def list_cargoes(db: Session = Depends(get_db)):
    logger.info("Listing all cargoes")
    return services.logistics.list_cargoes(db)

@app.get("/cargoes/{cargo_id}", response_model=schemas.cargo.Cargo)
def get_cargo(cargo_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching cargo with ID: {cargo_id}")
    cargo_obj = services.logistics.get_cargo(db, cargo_id)
    if not cargo_obj:
        logger.warning(f"Cargo {cargo_id} not found")
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo_obj


# --- Tracking ---

@app.get("/trackings/{cargo_id}", response_model=List[schemas.tracking.Tracking])
def get_tracking_for_cargo(cargo_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching tracking for cargo ID: {cargo_id}")
    return services.logistics.get_tracking_for_cargo(db, cargo_id)