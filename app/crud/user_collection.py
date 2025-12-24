from sqlalchemy.orm import Session
from app.models.user_manga_volumes import UserMangaVolume
from app.schemas.user_collection import UserCollectionAdd, UserCollectionUpdate
from datetime import datetime, timezone


def add_to_collection(db: Session, user_id: int, collection_data: UserCollectionAdd) -> UserMangaVolume:
    """Añade un tomo a la colección del usuario"""
    db_collection = UserMangaVolume(
        user_id=user_id,
        volume_id=collection_data.volume_id,
        is_owned=collection_data.is_owned,
        is_reading=collection_data.is_reading,
        is_completed=collection_data.is_completed,
        is_wishlist=collection_data.is_wishlist,
        purchase_price=collection_data.purchase_price,
        purchase_date=collection_data.purchase_date,
        condition=collection_data.condition,
        notes=collection_data.notes
    )

    # Fechas automáticas
    if collection_data.is_reading:
        db_collection.started_reading_at = datetime.now(timezone.utc)

    if collection_data.is_completed:
        db_collection.completed_reading_at = datetime.now(timezone.utc)

    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection


def get_user_collection(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[UserMangaVolume]:
    """Obtiene toda la colección de un usuario"""
    return db.query(UserMangaVolume).filter(UserMangaVolume.user_id == user_id).offset(skip).limit(limit).all() # type: ignore


def get_collection_entry(db: Session, user_id: int, volume_id: int) -> UserMangaVolume | None:
    """Obtiene una entrada específica de la colección"""
    return db.query(UserMangaVolume).filter(
        UserMangaVolume.user_id == user_id,
        UserMangaVolume.volume_id == volume_id
    ).first()


def update_collection_entry(
        db: Session,
        user_id: int,
        volume_id: int,
        update_data: UserCollectionUpdate
) -> UserMangaVolume | None:
    """Actualiza una entrada de la colección"""
    db_collection = get_collection_entry(db, user_id, volume_id)

    if not db_collection:
        return None

    update_dict = update_data.model_dump(exclude_unset=True)

    # Lógica de fechas
    if update_data.is_reading and not db_collection.started_reading_at:
        update_dict['started_reading_at'] = datetime.now(timezone.utc)

    if update_data.is_completed and not db_collection.completed_reading_at:
        update_dict['completed_reading_at'] = datetime.now(timezone.utc)

    for key, value in update_dict.items():
        setattr(db_collection, key, value)

    db.commit()
    db.refresh(db_collection)
    return db_collection


def remove_from_collection(db: Session, user_id: int, volume_id: int) -> bool:
    """Elimina un tomo de la colección"""
    db_collection = get_collection_entry(db, user_id, volume_id)

    if not db_collection:
        return False

    db.delete(db_collection)
    db.commit()
    return True


def get_user_wishlist(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[UserMangaVolume]:
    """Obtiene la wishlist del usuario"""
    return db.query(UserMangaVolume).filter(UserMangaVolume.user_id == user_id,UserMangaVolume.is_wishlist == True).offset(skip).limit(limit).all() # type: ignore


def get_user_reading(db: Session, user_id: int) -> list[UserMangaVolume]:
    """Obtiene los tomos que el usuario está leyendo"""
    return db.query(UserMangaVolume).filter(UserMangaVolume.user_id == user_id,UserMangaVolume.is_reading == True).all() # type: ignore


def get_user_owned(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[UserMangaVolume]:
    """Obtiene los tomos que el usuario posee"""
    return db.query(UserMangaVolume).filter(UserMangaVolume.user_id == user_id,UserMangaVolume.is_owned == True).offset(skip).limit(limit).all() # type: ignore