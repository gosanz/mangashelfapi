from sqlalchemy.orm import Session
from app.models.user_manga import UserManga
from app.schemas.collection import CollectionAddManga, CollectionUpdateManga
from datetime import datetime, timezone

def add_to_collection(db: Session, user_id: int, manga_data: CollectionAddManga) -> UserManga:
    db_collection = UserManga(
        user_id = user_id,
        manga_id = manga_data.manga_id,
        is_owned = manga_data.is_owned,
        is_reading = manga_data.is_reading,
        is_completed = manga_data.is_completed,
        is_wishlist = manga_data.is_wishlist,
        volumes_owned = manga_data.volumes_owned,
        notes = manga_data.notes
    )

    if manga_data.is_reading:
        db_collection.started_reading_at = datetime.now(timezone.utc)

    if manga_data.is_completed:
        db_collection.completed_reading_at = datetime.now(timezone.utc)

    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)

    return db_collection

def get_user_collection(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[UserManga]:
    return db.query(UserManga).filter(UserManga.user_id == user_id).offset(skip).limit(limit).all() # type: ignore

def get_collection_entry(db: Session, user_id: int, manga_id: int) -> UserManga | None:
    return db.query(UserManga).filter(UserManga.user_id == user_id, UserManga.manga_id == manga_id).first()

def update_collection_entry(db: Session, user_id: int, manga_id: int, update_data: CollectionUpdateManga) -> UserManga | None:
    db_collection = get_collection_entry(db, user_id, manga_id)
    if not db_collection:
        return None

    update_dict = update_data.model_dump(exclude_unset=True)

    if update_data.is_reading and not db_collection.started_reading_at:
        update_dict['started_reading_at'] = datetime.now(timezone.utc)

    if update_data.is_completed and not db_collection.completed_reading_at:
        update_dict['completed_reading_at'] = datetime.now(timezone.utc)

    for k, v in update_dict.items():
        setattr(db_collection, k, v)

    db.commit()
    db.refresh(db_collection)
    return db_collection

def remove_from_collection(db: Session, user_id: int, manga_id: int) -> bool:
    db_collection = get_collection_entry(db, user_id, manga_id)
    if not db_collection:
        return False

    db.delete(db_collection)
    db.commit()
    return True

def get_user_wishlist(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[UserManga]:
    return db.query(UserManga).filter(UserManga.user_id == user_id, UserManga.is_wishlist == True).offset(skip).limit(limit).all() # type: ignore

def get_user_reading(db: Session, user_id:int) -> list[UserManga]:
    return db.query(UserManga).filter(UserManga.user_id == user_id, UserManga.is_reading == True).all() # type: ignore
