from sqlalchemy.orm import Session
from app.models.manga_volumes import MangaVolume
from app.schemas.manga_volumes import MangaVolumeCreate

def create_volume(db: Session, volume: MangaVolumeCreate) -> MangaVolume:
    """Crea un tomo de manga"""
    db_volume = MangaVolume(
        series_id=volume.series_id,
        volume_number=volume.volume_number,
        isbn=volume.isbn,
        title=volume.title,
        pages=volume.pages,
        chapters=volume.chapters,
        release_date=volume.release_date,
        cover_image_url=volume.cover_image_url
    )
    db.add(db_volume)
    db.commit()
    db.refresh(db_volume)
    return db_volume


def create_volumes_bulk(db: Session, volumes: list[MangaVolumeCreate]) -> list[MangaVolume]:
    """Crea múltiples tomos de una vez (bulk insert)"""
    db_volumes = [
        MangaVolume(
            series_id=volume.series_id,
            volume_number=volume.volume_number,
            isbn=volume.isbn,
            title=volume.title,
            pages=volume.pages,
            chapters=volume.chapters,
            release_date=volume.release_date,
            cover_image_url=volume.cover_image_url
        )
        for volume in volumes
    ]

    db.add_all(db_volumes)
    db.commit()

    for volume in db_volumes:
        db.refresh(volume)

    return db_volumes


def get_volume_by_id(db: Session, volume_id: int) -> MangaVolume | None:
    """Busca un tomo por ID"""
    return db.query(MangaVolume).filter(MangaVolume.id == volume_id).first()


def get_volume_by_isbn(db: Session, isbn: str) -> MangaVolume | None:
    """Busca un tomo por ISBN (para escaneo)"""
    return db.query(MangaVolume).filter(MangaVolume.isbn == isbn).first()


def get_volumes_by_series(db: Session, series_id: int, skip: int = 0, limit: int = 200) -> list[MangaVolume]:
    """Obtiene todos los tomos de una serie"""
    return db.query(MangaVolume).filter(MangaVolume.series_id == series_id).order_by(MangaVolume.volume_number).offset(skip).limit(limit).all() # type: ignore


def search_volumes(db: Session, query: str, skip: int = 0, limit: int = 20) -> list[MangaVolume]:
    """Busca tomos por título o ISBN"""
    search_pattern = f"%{query}%"
    return db.query(MangaVolume).filter((MangaVolume.title.ilike(search_pattern)) | (MangaVolume.isbn.ilike(search_pattern))).offset(skip).limit(limit).all() # type: ignore

def get_all_volumes(db: Session, skip: int = 0, limit: int = 100) -> list[MangaVolume]:
    """Get all mangas with pagination"""
    return db.query(MangaVolume).offset(skip).limit(limit).all() # type: ignore