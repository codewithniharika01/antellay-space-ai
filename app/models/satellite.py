from sqlalchemy import Column, Integer, String

from app.database.database import Base


class Satellite(Base):
    __tablename__ = "satellites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    norad_id = Column(Integer, unique=True, nullable=False, index=True)
    country = Column(String, nullable=False)
    mission = Column(String, nullable=False)
    status = Column(String, nullable=False)