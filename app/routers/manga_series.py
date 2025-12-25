from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.manga_series import MangaSeriesCreate, MangaSeriesResponse
from app.crud import manga_series as crud_series
from app.dependencies.auth import get_current_active_user, get_current_admin_user
from app.models.user import User

router = APIRouter(
    prefix="/series",
    tags=["Manga Series"]
)


@router.post("/", response_model=MangaSeriesResponse, status_code=status.HTTP_201_CREATED)
def create_series(
        series: MangaSeriesCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_admin_user)
):
    """Crea una serie de manga"""
    return crud_series.create_series(db, series)


@router.get("/search", response_model=list[MangaSeriesResponse])
def search_series(
        q: str = Query(..., min_length=1, description="Search query"),
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Busca series por título o autor"""
    return crud_series.search_series(db, q, skip, limit)


@router.get("/publisher/{publisher_id}", response_model=list[MangaSeriesResponse])
def get_series_by_publisher(
        publisher_id: int,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Obtiene series de una editorial específica"""
    return crud_series.get_series_by_publisher(db, publisher_id, skip, limit)


@router.get("/{series_id}", response_model=MangaSeriesResponse)
def get_series(
        series_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Obtiene una serie por ID"""
    series = crud_series.get_series_by_id(db, series_id)

    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Series not found"
        )

    return series


@router.get("/", response_model=list[MangaSeriesResponse])
def list_series(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Lista todas las series"""
    return crud_series.get_all_series(db, skip, limit)