from fastapi import FastAPI
from app.routers import contract_router, tracking_router, cargo_router, vessel_router


app = FastAPI(title="Shipping Logistics API", version="1.0")

app.include_router(contract_router)
app.include_router(cargo_router)
app.include_router(tracking_router)
app.include_router(vessel_router)
