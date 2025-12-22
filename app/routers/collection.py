from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.collection import CollectionAddManga, CollectionUpdateManga, CollectionResponse
from app.crud import user_manga as crud_collection
from app.crud import manga as crud_manga
from app.dependencies.auth import get_current_active_user
from app.models.user import User

router = APIRouter(
    prefix="/collection",
    tags=["Collection"]
)


@router.post("/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
def add_manga_to_collection(
        manga_data: CollectionAddManga,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    manga = crud_manga.get_manga_by_id(db, manga_data.manga_id)
    if not manga:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manga not found"
        )

    existing = crud_collection.get_collection_entry(db, current_user.id, manga_data.manga_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Manga already in collection"
        )

    return crud_collection.add_to_collection(db, current_user.id, manga_data)


@router.get("/", response_model=list[CollectionResponse])
def get_my_collection(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):

    return crud_collection.get_user_collection(db, current_user.id, skip, limit)


@router.get("/wishlist", response_model=list[CollectionResponse])
def get_my_wishlist(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):

    return crud_collection.get_user_wishlist(db, current_user.id, skip, limit)


@router.get("/reading", response_model=list[CollectionResponse])
def get_currently_reading(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):

    return crud_collection.get_user_reading(db, current_user.id)


@router.get("/{manga_id}", response_model=CollectionResponse)
def get_collection_entry(
        manga_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):

    entry = crud_collection.get_collection_entry(db, current_user.id, manga_id)

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manga not in collection"
        )

    return entry


@router.patch("/{manga_id}", response_model=CollectionResponse)
def update_collection_entry(
        manga_id: int,
        update_data: CollectionUpdateManga,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):

    updated = crud_collection.update_collection_entry(db, current_user.id, manga_id, update_data)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manga not in collection"
        )

    return updated


@router.delete("/{manga_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_manga_from_collection(
        manga_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):

    success = crud_collection.remove_from_collection(db, current_user.id, manga_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manga not in collection"
        )

    return None