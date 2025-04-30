from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Tracking(Base):
    __tablename__ = "trackings"

    id = Column(Integer, primary_key=True, index=True)
    cargo_id = Column(Integer, ForeignKey("cargoes.id"), nullable=False)
    location = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    cargo = relationship("Cargo", back_populates="tracking")
