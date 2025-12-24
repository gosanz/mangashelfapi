from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    country = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relación con series
    series = relationship("MangaSeries", back_populates="publisher")