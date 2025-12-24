from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class MangaSeries(Base):
    __tablename__ = "manga_series"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=True, index=True)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=True)
    edition_type = Column(String, nullable=True)
    total_volumes = Column(Integer, nullable=True)
    is_completed = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    cover_image_url = Column(String, nullable=True)
    started_publication_date = Column(Date, nullable=True)
    ended_publication_date = Column(Date, nullable=True)

    # Relaciones
    publisher = relationship("Publisher", back_populates="series")
    volumes = relationship("MangaVolume", back_populates="series", cascade="all, delete-orphan")