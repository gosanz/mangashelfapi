from pydantic import BaseModel


class MangaCreate(BaseModel):
    title: str
    author: str | None = None
    publisher: str | None = None
    isbn: str | None = None
    description:str | None = None
    cover_image_url: str | None = None
    volumes_total: int | None = None


class MangaResponse(BaseModel):
    id: int
    title: str
    author: str | None
    publisher: str | None
    isbn: str | None
    description: str | None
    cover_image_url: str | None
    volumes_total: int | None

    class Config:
        from_attributes = True

class MangaISBN(BaseModel):
    isbn: str