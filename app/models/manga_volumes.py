from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class MangaVolume(Base):
    __tablename__ = "manga_volumes"

    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey("manga_series.id", ondelete="CASCADE"), nullable=False)
    volume_number = Column(Integer, nullable=False)
    isbn = Column(String, unique=True, nullable=True, index=True)
    title = Column(String, nullable=True)
    pages = Column(Integer, nullable=True)
    chapters = Column(String, nullable=True)
    release_date = Column(Date, nullable=True)
    cover_image_url = Column(String, nullable=True)

    # Constraint: No puede haber dos tomos con el mismo número en la misma serie
    __table_args__ = (
        UniqueConstraint('series_id', 'volume_number', name='unique_series_volume'),
    )

    # Relaciones
    series = relationship("MangaSeries", back_populates="volumes")
    user_collections = relationship("UserMangaVolume", back_populates="volume", cascade="all, delete-orphan")