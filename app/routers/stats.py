from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.stats import CollectionStatsResponse, PublisherStatsResponse, AuthorStatsResponse
from app.crud.stats import get_collection_stats, get_top_authors, get_top_publishers
from app.dependencies.auth import get_current_active_user
from app.models.user import User

router = APIRouter(
    prefix="/stats",
    tags=["Statistics"]
)

@router.get("/collection", response_model=CollectionStatsResponse)
def get_my_collection_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtiene estadísticas generales de la colección del usuario"""
    return get_collection_stats(db, current_user.id)

@router.get("/publishers", response_model=list[PublisherStatsResponse])
def get_my_top_publishers(
    limit: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtiene las editoriales más frecuentes en tu colección"""
    return get_top_publishers(db, current_user.id, limit)

@router.get("/authors", response_model=list[AuthorStatsResponse])
def get_my_top_authors(
    limit: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtiene los autores más frecuentes en tu colección"""
    return get_top_authors(db, current_user.id, limit)