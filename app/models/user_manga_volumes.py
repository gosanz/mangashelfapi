from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, Text, Numeric, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class UserMangaVolume(Base):
    __tablename__ = "user_manga_volumes"

    # Clave primaria compuesta
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    volume_id = Column(Integer, ForeignKey("manga_volumes.id", ondelete="CASCADE"), primary_key=True)

    # Estados
    is_owned = Column(Boolean, default=False)
    is_reading = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    is_wishlist = Column(Boolean, default=False)

    # Metadata
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    started_reading_at = Column(DateTime(timezone=True), nullable=True)
    completed_reading_at = Column(DateTime(timezone=True), nullable=True)

    # Información de compra (opcional)
    purchase_price = Column(Numeric(10, 2), nullable=True)
    purchase_date = Column(Date, nullable=True)
    condition = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    # Relaciones
    user = relationship("User", back_populates="collection")
    volume = relationship("MangaVolume", back_populates="user_collections")