from pydantic import BaseModel
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.manga import MangaResponse

class CollectionAdd(BaseModel):
    manga_id: int
    is_owned: bool = False
    is_reading: bool = False
    is_completed: bool = False
    is_wishlist: bool = False
    volumes_owned: int = 0
    notes: str | None = None


class CollectionUpdate(BaseModel):
    is_owned: bool | None = None
    is_reading: bool | None = None
    is_completed: bool | None = None
    is_wishlist: bool | None = None
    volumes_owned: int | None = None
    is_collection_complete: bool | None = None
    notes: str | None = None
    started_reading_at: datetime | None = None
    completed_reading_at: datetime | None = None


class CollectionResponse(BaseModel):
    user_id: int
    manga_id: int
    is_owned: bool
    is_reading: bool
    is_completed: bool
    is_wishlist: bool
    volumes_owned: int
    is_collection_complete: bool
    added_at: datetime
    started_reading_at: datetime | None
    completed_reading_at: datetime | None
    notes: str | None
    manga: "MangaResponse"

    class Config:
        from_attributes = True


from app.schemas.manga import MangaResponse
CollectionResponse.model_rebuild()

