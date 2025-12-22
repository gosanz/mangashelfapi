from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.manga import MangaCreate, MangaResponse
from app.models.user import User
from app.dependencies.auth import get_current_active_user
from app.crud import manga as crud_manga


router = APIRouter(
    prefix="/mangas",
    tags=["Mangas"]
)


@router.post("/", response_model=MangaResponse, status_code=status.HTTP_201_CREATED)
def create_manga(manga: MangaCreate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_active_user)
):
    if manga.isbn:
        if crud_manga.get_manga_by_isbn(db, manga.isbn):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Manga with ISBN {manga.isbn} already exists")

    return crud_manga.create_manga(db, manga)


@router.get("/search", response_model=list[MangaResponse])
def search_mangas(q: str = Query(..., min_length=1, description="Search Query"),
                  skip: int = Query(0, ge=0),
                  limit: int = Query(20, ge=1, le=100),
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_active_user)
):
    return crud_manga.search_mangas(db, q, skip, limit)


@router.get("/isbn/{isbn}", response_model=MangaResponse)
def get_manga_by_isbn(
        isbn: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    manga = crud_manga.get_manga_by_isbn(db, isbn)

    if not manga:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manga not found"
        )

    return manga


@router.get("/{manga_id}", response_model=MangaResponse)
def get_manga(
        manga_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    manga = crud_manga.get_manga_by_id(db, manga_id)

    if not manga:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manga not found"
        )

    return manga


@router.get("/", response_model=list[MangaResponse])
def list_mangas(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    return crud_manga.get_all_mangas(db, skip, limit)