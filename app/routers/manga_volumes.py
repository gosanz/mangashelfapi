from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.manga_volumes import MangaVolumeCreate, MangaVolumeResponse
from app.crud import manga_volumes as crud_volumes
from app.dependencies.auth import get_current_active_user, get_current_admin_user
from app.models.user import User

router = APIRouter(
    prefix="/volumes",
    tags=["Manga Volumes"]
)


@router.post("/", response_model=MangaVolumeResponse, status_code=status.HTTP_201_CREATED)
def create_volume(
        volume: MangaVolumeCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_admin_user)
):
    """Crea un tomo de manga"""
    # Verificar si ya existe por ISBN
    if volume.isbn:
        existing = crud_volumes.get_volume_by_isbn(db, volume.isbn)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Volume with this ISBN already exists"
            )

    return crud_volumes.create_volume(db, volume)


@router.post("/bulk", response_model=list[MangaVolumeResponse], status_code=status.HTTP_201_CREATED)
def create_volumes_bulk(
        volumes: list[MangaVolumeCreate],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_admin_user)
):
    """Crea múltiples tomos de una vez (bulk insert)"""
    return crud_volumes.create_volumes_bulk(db, volumes)


@router.get("/search", response_model=list[MangaVolumeResponse])
def search_volumes(
        q: str = Query(..., min_length=1, description="Search query"),
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Busca tomos por título o ISBN"""
    return crud_volumes.search_volumes(db, q, skip, limit)


@router.get("/isbn/{isbn}", response_model=MangaVolumeResponse)
def get_volume_by_isbn(
        isbn: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Obtiene un tomo por ISBN (para escaneo)"""
    volume = crud_volumes.get_volume_by_isbn(db, isbn)

    if not volume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volume not found"
        )

    return volume


@router.get("/series/{series_id}", response_model=list[MangaVolumeResponse])
def get_volumes_by_series(
        series_id: int,
        skip: int = Query(0, ge=0),
        limit: int = Query(200, ge=1, le=200),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Obtiene todos los tomos de una serie"""
    return crud_volumes.get_volumes_by_series(db, series_id, skip, limit)


@router.get("/{volume_id}", response_model=MangaVolumeResponse)
def get_volume(
        volume_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Obtiene un tomo por ID"""
    volume = crud_volumes.get_volume_by_id(db, volume_id)

    if not volume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volume not found"
        )

    return volume