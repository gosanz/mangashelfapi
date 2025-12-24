from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import UserMangaVolume, MangaVolume



def get_collection_stats(db: Session, user_id: int) -> dict:
    # Total de mangas en colección
    total_mangas = db.query(UserMangaVolume).filter(UserMangaVolume.user_id == user_id).count()
    # Total de mangas owned (físicos)
    owned_count = db.query(UserMangaVolume).filter(UserMangaVolume.user_id == user_id, UserMangaVolume.is_owned == True).count()
    # Total de mangas en wishlist
    wishlist_count = db.query(UserMangaVolume).filter(UserMangaVolume.user_id == user_id, UserMangaVolume.is_wishlist == True).count()
    # Total de mangas leyendo
    reading_count = db.query(UserMangaVolume).filter(UserMangaVolume.user_id == user_id, UserMangaVolume.is_reading == True).count()
    # Total de mangas completados
    completed_count = db.query(UserMangaVolume).filter(UserMangaVolume.user_id == user_id, UserMangaVolume.is_completed == True).count()
    # Total de tomos poseídos
    total_volumes = db.query(func.sum(UserMangaVolume.volumes_owned)).filter(UserMangaVolume.user_id == user_id).scalar() or 0
    #  Colecciones completas
    complete_collections = db.query(UserMangaVolume).filter(UserMangaVolume.user_id == user_id, UserMangaVolume.is_collection_complete == True).count()

    return {
        "total_mangas": total_mangas,
        "owned_count": owned_count,
        "wishlist_count": wishlist_count,
        "reading_count": reading_count,
        "completed_count": completed_count,
        "total_volumes": total_volumes,
        "complete_collections": complete_collections
    }



def get_top_publishers(db: Session, user_id: int, limit: int = 10) -> list[dict]:
    results = db.query(
        UserMangaVolume.publisher, func.count(UserMangaVolume.manga_id).label('count')
    ).join(
        UserMangaVolume, UserMangaVolume.manga_id == UserMangaVolume.id
    ).filter(
        UserMangaVolume.user_id == user_id, UserMangaVolume.publisher.isnot(None)
    ).group_by(
        UserMangaVolume.publisher
    ).order_by(
        func.count(UserMangaVolume.manga_id).desc()
    ).limit(limit).all()

    return [{"publisher": pub, "count": count} for pub, count in results]


def get_top_authors(db: Session, user_id: int, limit: int = 10) -> list[dict]:
    results = db.query(
        UserMangaVolume.author,
        func.count(UserMangaVolume.manga_id).label('count')
    ).join(
        UserMangaVolume, UserMangaVolume.manga_id == UserMangaVolume.id
    ).filter(
        UserMangaVolume.user_id == user_id,
        UserMangaVolume.author.isnot(None)
    ).group_by(
        UserMangaVolume.author
    ).order_by(
        func.count(UserMangaVolume.manga_id).desc()
    ).limit(limit).all()

    return [{"author": author, "count": count} for author, count in results]