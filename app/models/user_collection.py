from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class UserCollection(Base):
    __tablename__ = "user_collections"

    # Primary key
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    manga_id = Column(Integer, ForeignKey("mangas.id"), primary_key=True)

    # States
    is_owned = Column(Boolean, default=False)
    is_reading = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    is_wishlist = Column(Boolean, default=False)

    # Collection info
    volumes_owned = Column(Integer, default=0)
    is_collection_complete = Column(Boolean, default=False)

    # Metadata
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    started_reading_at = Column(DateTime(timezone=True), nullable=True)
    completed_reading_at = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)

    # Relations
    user = relationship("User", back_populates="collections")
    manga = relationship("Manga", back_populates="collections")