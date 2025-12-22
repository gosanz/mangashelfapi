from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Manga(Base):
    __tablename__ = "mangas"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    #Manga info
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    isbn = Column(String, unique=True, nullable=True, index=True)
    description = Column(Text, nullable=True)
    cover_image_url = Column(String, nullable=True)
    volumes_total = Column(Integer, nullable=True)

    # Relations
    users = relationship("UserManga", back_populates="manga")