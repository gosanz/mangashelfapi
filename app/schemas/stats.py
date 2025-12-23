from pydantic import BaseModel

class CollectionStatsResponse(BaseModel):
    total_mangas: int
    owned_count: int
    wishlist_count: int
    reading_count: int
    completed_count: int
    total_volumes: int
    complete_collections: int

class PublisherStatsResponse(BaseModel):
    publisher: str
    count: int

class AuthorStatsResponse(BaseModel):
    author: str
    count: int