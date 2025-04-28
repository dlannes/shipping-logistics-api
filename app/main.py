from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, services
from app.db import SessionLocal, engine, Base
from app.logger import logger


Base.metadata.create_all(bind=engine)  # TODO
app = FastAPI(title="Shipping Logistics API", version="1.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contracts/", response_model=schemas.contract.Contract)
def create_contract(
    contract: schemas.contract.ContractCreate, db: Session = Depends(get_db)
):
    logger.info(f"Creating contract for client: {contract.client_name}")
    return services.contract.create_contract(db, contract)


@app.get("/contracts/{contract_id}", response_model=schemas.contract.Contract)
def read_contract(contract_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching contract with ID: {contract_id}")
    db_contract = services.contract.get_contract(db, contract_id)
    if not db_contract:
        logger.warning(f"Contract ID {contract_id} not found.")
        raise HTTPException(status_code=404, detail="Contract not found")
    return db_contract


@app.get("/contracts/", response_model=List[schemas.contract.Contract])
def list_contracts(db: Session = Depends(get_db)):
    logger.info("Listing all contracts")
    return services.contract.list_contracts(db)


@app.post("/cargos/", response_model=schemas.cargo.Cargo)
def create_cargo(cargo: schemas.cargo.CargoCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating cargo linked to contract ID: {cargo.contract_id}")
    return services.cargo.create_cargo(db, cargo)


@app.get("/cargos/{cargo_id}", response_model=schemas.cargo.Cargo)
def read_cargo(cargo_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching cargo with ID: {cargo_id}")
    db_cargo = services.cargo.get_cargo(db, cargo_id)
    if not db_cargo:
        logger.warning(f"Cargo ID {cargo_id} not found.")
        raise HTTPException(status_code=404, detail="Cargo not found")
    return db_cargo


@app.get("/cargos/", response_model=List[schemas.cargo.Cargo])
def list_cargos(db: Session = Depends(get_db)):
    logger.info("Listing all cargos")
    return services.cargo.list_cargos(db)


@app.post("/vessels/", response_model=schemas.vessel.Vessel)
def create_vessel(vessel: schemas.vessel.VesselCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating vessel: {vessel.name}")
    return services.vessel.create_vessel(db, vessel)


@app.get("/vessels/{vessel_id}", response_model=schemas.vessel.Vessel)
def read_vessel(vessel_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching vessel with ID: {vessel_id}")
    db_vessel = services.vessel.get_vessel(db, vessel_id)
    if not db_vessel:
        logger.warning(f"Vessel ID {vessel_id} not found.")
        raise HTTPException(status_code=404, detail="Vessel not found")
    return db_vessel


@app.get("/vessels/", response_model=List[schemas.vessel.Vessel])
def list_vessels(db: Session = Depends(get_db)):
    logger.info("Listing all vessels")
    return services.vessel.list_vessels(db)


@app.post("/trackings/", response_model=schemas.tracking.Tracking)
def create_tracking(
    tracking: schemas.tracking.TrackingCreate, db: Session = Depends(get_db)
):
    logger.info(
        f"Creating tracking entry for cargo ID: {tracking.cargo_id} at location: {tracking.location}"
    )
    return services.tracking.create_tracking(db, tracking)


@app.get("/trackings/{tracking_id}", response_model=schemas.tracking.Tracking)
def read_tracking(tracking_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching tracking with ID: {tracking_id}")
    db_tracking = services.tracking.get_tracking(db, tracking_id)
    if not db_tracking:
        logger.warning(f"Tracking ID {tracking_id} not found.")
        raise HTTPException(status_code=404, detail="Tracking not found")
    return db_tracking


@app.get("/trackings/", response_model=List[schemas.tracking.Tracking])
def list_trackings(db: Session = Depends(get_db)):
    logger.info("Listing all tracking entries")
    return services.tracking.list_trackings(db)
