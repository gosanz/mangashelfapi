from sqlalchemy.orm import Session
from app.models.manga import Manga
from app.schemas.manga import MangaCreate


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

def create_mangas_bulk(db: Session, mangas: list[MangaCreate]) -> list[Manga]:
    """Creates multiple mangas in the db"""

    db_mangas = [
        Manga(
            title=manga.title,
            author=manga.author,
            publisher=manga.publisher,
            isbn=manga.isbn,
            description=manga.description,
            cover_image_url=manga.cover_image_url,
            volumes_total=manga.volumes_total
        )
    for manga in mangas
    ]

    db.add_all(db_mangas)
    db.commit()
    for manga in db_mangas:
        db.refresh(manga)


    return db_mangas

def get_manga_by_id(db: Session, manga_id: int) -> Manga | None:
    """Searches manga by id"""
    return db.query(Manga).filter(Manga.id == manga_id).first()

def get_manga_by_isbn(db: Session, isbn: str) -> Manga | None:
    """Searches manga by isbn"""
    return db.query(Manga).filter(Manga.isbn == isbn).first()

def search_mangas(db: Session, query: str, skip: int = 0, limit: int = 1000) -> list[Manga]:
    """Searches all mangas by title or author"""
    return db.query(Manga).filter( # type: ignore
        (Manga.title.ilike(f"%{query}%")) | (Manga.author.ilike(f"%{query}%"))
    ).offset(skip).limit(limit).all()

def get_all_mangas(db: Session, skip: int = 0, limit: int = 1000) -> list[Manga]:
    """Get all mangas with pagination"""
    return db.query(Manga).offset(skip).limit(limit).all() # type: ignore