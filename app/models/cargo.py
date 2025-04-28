from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Cargo(Base):
    __tablename__ = "cargos"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    status = Column(String, default="pending")

    contract = relationship("Contract", back_populates="cargos")
    tracking_history = relationship("Tracking", back_populates="cargo")
