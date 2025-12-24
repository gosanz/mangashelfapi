from sqlalchemy.orm import Session
from app.models.publishers import Publisher
from app.schemas.publishers import PublisherCreate

def create_publisher(db: Session, publisher: PublisherCreate) -> Publisher:
    """Crea una editorial"""
    db_publisher = Publisher(
        name=publisher.name,
        country=publisher.country,
        is_active=publisher.is_active
    )
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher

def get_publisher_by_id(db: Session, publisher_id: int) -> Publisher | None:
    """Busca una editorial por ID"""
    return db.query(Publisher).filter(Publisher.id == publisher_id).first()

def get_publisher_by_name(db: Session, name: str) -> Publisher | None:
    """Busca una editorial por nombre"""
    return db.query(Publisher).filter(Publisher.name == name).first()

def get_all_publishers(db: Session, skip: int = 0, limit: int = 100) -> list[Publisher]:
    """Obtiene todas las editoriales (paginado)"""
    return db.query(Publisher).offset(skip).limit(limit).all() # type: ignore

def search_publishers(db: Session, query: str, skip: int = 0, limit: int = 20) -> list[Publisher]:
    """Busca editoriales por nombre"""
    search_pattern = f"%{query}%"
    return db.query(Publisher).filter(Publisher.name.ilike(search_pattern)).offset(skip).limit(limit).all() # type: ignore