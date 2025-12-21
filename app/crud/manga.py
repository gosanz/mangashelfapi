from sqlalchemy.orm import Session
from app.models.manga import Manga
from app.schemas.manga import MangaCreate
from typing import Optional, List


def create_manga(db: Session, manga: MangaCreate) -> Manga:
    """Creates a manga in the db"""

    db_manga = Manga(
        title = manga.title,
        author = manga.author,
        publisher = manga.publisher,
        isbn = manga.isbn,
        description = manga.description,
        cover_image_url = manga.cover_image_url,
        volumes_total = manga.volumes_total
    )

    db.add(db_manga)
    db.commit()
    db.refresh(db_manga)

    return db_manga

def update_manga(db: Session, manga: MangaCreate) -> Manga:
    pass

def delete_manga(db: Session, title) -> bool:
    db.delete(title)
    db.commit()
    db.refresh(title)

    return True

def get_manga_by_isbn(db: Session, isbn: str) -> Optional[Manga]:
    """Searches manga by isbn"""
    return db.query(Manga).filter(Manga.isbn == isbn).first()

def get_manga_by_title(db: Session, title: str) -> Optional[Manga]:
    """Searches manga by title"""
    return db.query(Manga).filter(Manga.title == title).first()

def get_mangas_by_author(db: Session, author: str) -> List[Manga]:
    """Searches all mangas by author"""
    return db.query(Manga).filter(Manga.author == author).all() # type: ignore