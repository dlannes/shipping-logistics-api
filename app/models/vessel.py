from sqlalchemy import Column, Integer, String
from app.db import Base

class Vessel(Base):
    __tablename__ = "vessels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    current_location = Column(String, nullable=False)
