from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import UserManga, Manga



def get_collection_stats(db: Session, user_id: int) -> dict:
    # Total de mangas en colección
    total_mangas = db.query(UserManga).filter(UserManga.user_id == user_id).count()
    # Total de mangas owned (físicos)
    owned_count = db.query(UserManga).filter(UserManga.user_id == user_id, UserManga.is_owned == True).count()
    # Total de mangas en wishlist
    wishlist_count = db.query(UserManga).filter(UserManga.user_id == user_id, UserManga.is_wishlist == True).count()
    # Total de mangas leyendo
    reading_count = db.query(UserManga).filter(UserManga.user_id == user_id, UserManga.is_reading == True).count()
    # Total de mangas completados
    completed_count = db.query(UserManga).filter(UserManga.user_id == user_id, UserManga.is_completed == True).count()
    # Total de tomos poseídos
    total_volumes = db.query(func.sum(UserManga.volumes_owned)).filter(UserManga.user_id == user_id).scalar() or 0
    #  Colecciones completas
    complete_collections = db.query(UserManga).filter(UserManga.user_id == user_id, UserManga.is_collection_complete == True).count()

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
        Manga.publisher, func.count(UserManga.manga_id).label('count')
    ).join(
        UserManga, UserManga.manga_id == Manga.id
    ).filter(
        UserManga.user_id == user_id, Manga.publisher.isnot(None)
    ).group_by(
        Manga.publisher
    ).order_by(
        func.count(UserManga.manga_id).desc()
    ).limit(limit).all()

    return [{"publisher": pub, "count": count} for pub, count in results]


def get_top_authors(db: Session, user_id: int, limit: int = 10) -> list[dict]:
    results = db.query(
        Manga.author,
        func.count(UserManga.manga_id).label('count')
    ).join(
        UserManga, UserManga.manga_id == Manga.id
    ).filter(
        UserManga.user_id == user_id,
        Manga.author.isnot(None)
    ).group_by(
        Manga.author
    ).order_by(
        func.count(UserManga.manga_id).desc()
    ).limit(limit).all()

    return [{"author": author, "count": count} for author, count in results]