from pydantic import BaseModel

class PublisherCreate(BaseModel):
    name: str
    country: str | None = None
    is_active: bool = True

class PublisherResponse(BaseModel):
    id: int
    name: str
    country: str | None
    is_active: bool

    class Config:
        from_attributes = True