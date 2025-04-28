from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class Tracking(Base):
    __tablename__ = "trackings"

    id = Column(Integer, primary_key=True, index=True)
    cargo_id = Column(Integer, ForeignKey("cargos.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    location = Column(String, nullable=False)

    cargo = relationship("Cargo", back_populates="tracking_history")
