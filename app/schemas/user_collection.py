from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.manga_volumes import MangaVolumeResponse


class UserCollectionAdd(BaseModel):
    volume_id: int
    is_owned: bool = False
    is_reading: bool = False
    is_completed: bool = False
    is_wishlist: bool = False
    purchase_price: Decimal | None = None
    purchase_date: date | None = None
    condition: str | None = None
    notes: str | None = None


class UserCollectionUpdate(BaseModel):
    is_owned: bool | None = None
    is_reading: bool | None = None
    is_completed: bool | None = None
    is_wishlist: bool | None = None
    purchase_price: Decimal | None = None
    purchase_date: date | None = None
    condition: str | None = None
    notes: str | None = None
    started_reading_at: datetime | None = None
    completed_reading_at: datetime | None = None


class UserCollectionResponse(BaseModel):
    user_id: int
    volume_id: int
    is_owned: bool
    is_reading: bool
    is_completed: bool
    is_wishlist: bool
    added_at: datetime
    started_reading_at: datetime | None
    completed_reading_at: datetime | None
    purchase_price: Decimal | None
    purchase_date: date | None
    condition: str | None
    notes: str | None

    # Info del volumen (con serie anidada)
    volume: "MangaVolumeResponse"

    class Config:
        from_attributes = True


from app.schemas.manga_volumes import MangaVolumeResponse

UserCollectionResponse.model_rebuild()