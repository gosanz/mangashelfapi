from sqlalchemy.orm import Session
from app.models.manga_series import MangaSeries
from app.schemas.manga_series import MangaSeriesCreate

def create_series(db: Session, series: MangaSeriesCreate) -> MangaSeries:
    """Crea una serie de manga"""
    db_series = MangaSeries(
        title=series.title,
        author=series.author,
        publisher_id=series.publisher_id,
        edition_type=series.edition_type,
        total_volumes=series.total_volumes,
        is_completed=series.is_completed,
        description=series.description,
        cover_image_url=series.cover_image_url,
        started_publication_date=series.started_publication_date,
        ended_publication_date=series.ended_publication_date
    )
    db.add(db_series)
    db.commit()
    db.refresh(db_series)
    return db_series

def get_series_by_id(db: Session, series_id: int) -> MangaSeries | None:
    """Busca una serie por ID"""
    return db.query(MangaSeries).filter(MangaSeries.id == series_id).first()

def search_series(db: Session, query: str, skip: int = 0, limit: int = 20) -> list[MangaSeries]:
    """Busca series por título o autor"""
    search_pattern = f"%{query}%"
    return db.query(MangaSeries).filter((MangaSeries.title.ilike(search_pattern)) | (MangaSeries.author.ilike(search_pattern))).offset(skip).limit(limit).all() # type: ignore

def get_all_series(db: Session, skip: int = 0, limit: int = 100) -> list[MangaSeries]:
    """Obtiene todas las series (paginado)"""
    return db.query(MangaSeries).offset(skip).limit(limit).all() # type: ignore

def get_series_by_publisher(db: Session, publisher_id: int, skip: int = 0, limit: int = 100) -> list[MangaSeries]:
    """Obtiene series de una editorial específica"""
    return db.query(MangaSeries).filter(MangaSeries.publisher_id == publisher_id).offset(skip).limit(limit).all() # type: ignore
