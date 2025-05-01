from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Cargo(Base):
    __tablename__ = "cargoes"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    vessel_id = Column(Integer, ForeignKey("vessels.id"), nullable=True)
    status = Column(String, default="pending")
    current_location = Column(String, nullable=True)

    contract = relationship("Contract", back_populates="cargo")
    vessel = relationship("Vessel", back_populates="cargoes")
    tracking = relationship("Tracking", back_populates="cargo")

    @property
    def destination(self) -> str | None:
        return self.contract.destination if self.contract else None