from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.publishers import PublisherCreate, PublisherResponse
from app.crud import publishers as crud_publishers
from app.dependencies.auth import get_current_active_user
from app.models.user import User

router = APIRouter(
    prefix="/publishers",
    tags=["Publishers"]
)


@router.post("/", response_model=PublisherResponse, status_code=status.HTTP_201_CREATED)
def create_publisher(
        publisher: PublisherCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Crea una editorial"""
    # Verificar que no exista
    existing = crud_publishers.get_publisher_by_name(db, publisher.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Publisher already exists"
        )

    return crud_publishers.create_publisher(db, publisher)


@router.get("/search", response_model=list[PublisherResponse])
def search_publishers(
        q: str = Query(..., min_length=1, description="Search query"),
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Busca editoriales por nombre"""
    return crud_publishers.search_publishers(db, q, skip, limit)


@router.get("/{publisher_id}", response_model=PublisherResponse)
def get_publisher(
        publisher_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Obtiene una editorial por ID"""
    publisher = crud_publishers.get_publisher_by_id(db, publisher_id)

    if not publisher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publisher not found"
        )

    return publisher


@router.get("/", response_model=list[PublisherResponse])
def list_publishers(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Lista todas las editoriales"""
    return crud_publishers.get_all_publishers(db, skip, limit)