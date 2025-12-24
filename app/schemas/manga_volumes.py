from pydantic import BaseModel
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.manga_series import MangaSeriesResponse


class MangaVolumeCreate(BaseModel):
    series_id: int
    volume_number: int
    isbn: str | None = None
    title: str | None = None
    pages: int | None = None
    chapters: str | None = None
    release_date: date | None = None
    cover_image_url: str | None = None


class MangaVolumeResponse(BaseModel):
    id: int
    series_id: int
    volume_number: int
    isbn: str | None
    title: str | None
    pages: int | None
    chapters: str | None
    release_date: date | None
    cover_image_url: str | None

    # Opcional: incluir info de la serie
    series: "MangaSeriesResponse | None" = None

    class Config:
        from_attributes = True


from app.schemas.manga_series import MangaSeriesResponse

MangaVolumeResponse.model_rebuild()