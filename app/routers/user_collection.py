from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_collection import UserCollectionAdd, UserCollectionUpdate, UserCollectionResponse
from app.crud import user_collection as crud_collection
from app.crud import manga_volumes as crud_volumes
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.stats import (
    CollectionStatsResponse,
    PublisherStatsByVolumes,
    PublisherStatsBySeries,
    AuthorStatsByVolumes,
    AuthorStatsBySeries,
    SeriesProgress
)
from app.crud import stats as crud_stats

router = APIRouter(
    prefix="/collection",
    tags=["Collection"]
)


@router.post("/", response_model=UserCollectionResponse, status_code=status.HTTP_201_CREATED)
def add_volume_to_collection(
        collection_data: UserCollectionAdd,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Añade un tomo a la colección del usuario"""
    # Verificar que el volumen existe
    volume = crud_volumes.get_volume_by_id(db, collection_data.volume_id)
    if not volume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volume not found"
        )

    # Verificar que no esté ya en la colección
    existing = crud_collection.get_collection_entry(db, current_user.id, collection_data.volume_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Volume already in collection"
        )

    return crud_collection.add_to_collection(db, current_user.id, collection_data)


@router.get("/", response_model=list[UserCollectionResponse])
def get_my_collection(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Obtiene toda la colección del usuario actual"""
    return crud_collection.get_user_collection(db, current_user.id, skip, limit)


@router.get("/owned", response_model=list[UserCollectionResponse])
def get_owned_volumes(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Obtiene los tomos que el usuario posee físicamente"""
    return crud_collection.get_user_owned(db, current_user.id, skip, limit)


@router.get("/wishlist", response_model=list[UserCollectionResponse])
def get_my_wishlist(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Obtiene la wishlist del usuario actual"""
    return crud_collection.get_user_wishlist(db, current_user.id, skip, limit)


@router.get("/reading", response_model=list[UserCollectionResponse])
def get_currently_reading(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Obtiene los tomos que el usuario está leyendo actualmente"""
    return crud_collection.get_user_reading(db, current_user.id)


@router.get("/{volume_id}", response_model=UserCollectionResponse)
def get_collection_entry(
        volume_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Obtiene una entrada específica de la colección"""
    entry = crud_collection.get_collection_entry(db, current_user.id, volume_id)

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volume not in collection"
        )

    return entry


@router.patch("/{volume_id}", response_model=UserCollectionResponse)
def update_collection_entry(
        volume_id: int,
        update_data: UserCollectionUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Actualiza una entrada de la colección"""
    updated = crud_collection.update_collection_entry(db, current_user.id, volume_id, update_data)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volume not in collection"
        )

    return updated


@router.delete("/{volume_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_volume_from_collection(
        volume_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Elimina un tomo de la colección"""
    success = crud_collection.remove_from_collection(db, current_user.id, volume_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volume not in collection"
        )

    return None

# ========== ESTADÍSTICAS ==========

@router.get("/stats/summary", response_model=CollectionStatsResponse)
def get_collection_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtiene estadísticas generales de la colección"""
    return crud_stats.get_collection_stats(db, current_user.id)

@router.get("/stats/publishers/by-volumes", response_model=list[PublisherStatsByVolumes])
def get_top_publishers_by_volumes(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Top editoriales por número de tomos poseídos"""
    return crud_stats.get_top_publishers_by_volumes(db, current_user.id, limit)

@router.get("/stats/publishers/by-series", response_model=list[PublisherStatsBySeries])
def get_top_publishers_by_series(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Top editoriales por número de series diferentes"""
    return crud_stats.get_top_publishers_by_series(db, current_user.id, limit)

@router.get("/stats/authors/by-volumes", response_model=list[AuthorStatsByVolumes])
def get_top_authors_by_volumes(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Top autores por número de tomos poseídos"""
    return crud_stats.get_top_authors_by_volumes(db, current_user.id, limit)

@router.get("/stats/authors/by-series", response_model=list[AuthorStatsBySeries])
def get_top_authors_by_series(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Top autores por número de series diferentes"""
    return crud_stats.get_top_authors_by_series(db, current_user.id, limit)

@router.get("/stats/series-progress", response_model=list[SeriesProgress])
def get_series_progress(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtiene el progreso de colección por serie (cuántos tomos tienes de cada serie)"""
    return crud_stats.get_series_progress(db, current_user.id, limit)