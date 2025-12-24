from pydantic import BaseModel
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.publishers import PublisherResponse


class MangaSeriesCreate(BaseModel):
    title: str
    author: str | None = None
    publisher_id: int | None = None
    edition_type: str | None = None
    total_volumes: int | None = None
    is_completed: bool = False
    description: str | None = None
    cover_image_url: str | None = None
    started_publication_date: date | None = None
    ended_publication_date: date | None = None


class MangaSeriesResponse(BaseModel):
    id: int
    title: str
    author: str | None
    publisher_id: int | None
    edition_type: str | None
    total_volumes: int | None
    is_completed: bool
    description: str | None
    cover_image_url: str | None
    started_publication_date: date | None
    ended_publication_date: date | None

    # Opcional: incluir info del publisher
    publisher: "PublisherResponse | None" = None

    class Config:
        from_attributes = True


# Import para resolver forward reference
from app.schemas.publishers import PublisherResponse

MangaSeriesResponse.model_rebuild()