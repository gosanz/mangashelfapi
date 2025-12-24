from pydantic import BaseModel

class CollectionStatsResponse(BaseModel):
    total_volumes: int
    total_series: int
    owned_count: int
    wishlist_count: int
    reading_count: int
    completed_count: int
    total_spent: float

class PublisherStatsByVolumes(BaseModel):
    publisher: str
    total_volumes: int

class PublisherStatsBySeries(BaseModel):
    publisher: str
    series_count: int

class AuthorStatsByVolumes(BaseModel):
    author: str
    total_volumes: int

class AuthorStatsBySeries(BaseModel):
    author: str
    series_count: int

class SeriesProgress(BaseModel):
    series_id: int
    series_title: str
    edition_type: str | None
    total_volumes: int | None
    owned_volumes: int
    completion_percentage: float