from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.models.user_manga_volumes import UserMangaVolume
from app.models.manga_volumes import MangaVolume
from app.models.manga_series import MangaSeries
from app.models.publishers import Publisher


def get_collection_stats(db: Session, user_id: int) -> dict:
    """Obtiene estadísticas generales de la colección del usuario"""

    # Total de tomos en colección (cualquier estado)
    total_volumes = db.query(UserMangaVolume).filter(
        UserMangaVolume.user_id == user_id
    ).count()

    # Total de series diferentes
    total_series = db.query(distinct(MangaVolume.series_id)).join(
        UserMangaVolume, UserMangaVolume.volume_id == MangaVolume.id
    ).filter(
        UserMangaVolume.user_id == user_id
    ).count()

    # Tomos poseídos físicamente
    owned_count = db.query(UserMangaVolume).filter(
        UserMangaVolume.user_id == user_id,
        UserMangaVolume.is_owned == True
    ).count()

    # Tomos en wishlist
    wishlist_count = db.query(UserMangaVolume).filter(
        UserMangaVolume.user_id == user_id,
        UserMangaVolume.is_wishlist == True
    ).count()

    # Tomos leyendo
    reading_count = db.query(UserMangaVolume).filter(
        UserMangaVolume.user_id == user_id,
        UserMangaVolume.is_reading == True
    ).count()

    # Tomos completados
    completed_count = db.query(UserMangaVolume).filter(
        UserMangaVolume.user_id == user_id,
        UserMangaVolume.is_completed == True
    ).count()

    # Total gastado (suma de precios de compra)
    total_spent = db.query(func.sum(UserMangaVolume.purchase_price)).filter(
        UserMangaVolume.user_id == user_id,
        UserMangaVolume.purchase_price.isnot(None)
    ).scalar() or 0

    return {
        "total_volumes": total_volumes,
        "total_series": total_series,
        "owned_count": owned_count,
        "wishlist_count": wishlist_count,
        "reading_count": reading_count,
        "completed_count": completed_count,
        "total_spent": float(total_spent)
    }


def get_top_publishers_by_volumes(db: Session, user_id: int, limit: int = 5) -> list[dict]:
    """Obtiene las editoriales con más tomos poseídos"""

    results = db.query(
        Publisher.name,
        func.count(UserMangaVolume.volume_id).label('total_volumes')
    ).join(
        MangaSeries, MangaSeries.publisher_id == Publisher.id
    ).join(
        MangaVolume, MangaVolume.series_id == MangaSeries.id
    ).join(
        UserMangaVolume, UserMangaVolume.volume_id == MangaVolume.id
    ).filter(
        UserMangaVolume.user_id == user_id,
        UserMangaVolume.is_owned == True
    ).group_by(
        Publisher.name
    ).order_by(
        func.count(UserMangaVolume.volume_id).desc()
    ).limit(limit).all()

    return [{"publisher": name, "total_volumes": int(count)} for name, count in results]


def get_top_publishers_by_series(db: Session, user_id: int, limit: int = 5) -> list[dict]:
    """Obtiene las editoriales con más series diferentes"""

    results = db.query(
        Publisher.name,
        func.count(distinct(MangaSeries.id)).label('series_count')
    ).join(
        MangaSeries, MangaSeries.publisher_id == Publisher.id
    ).join(
        MangaVolume, MangaVolume.series_id == MangaSeries.id
    ).join(
        UserMangaVolume, UserMangaVolume.volume_id == MangaVolume.id
    ).filter(
        UserMangaVolume.user_id == user_id,
        UserMangaVolume.is_owned == True
    ).group_by(
        Publisher.name
    ).order_by(
        func.count(distinct(MangaSeries.id)).desc()
    ).limit(limit).all()

    return [{"publisher": name, "series_count": int(count)} for name, count in results]


def get_top_authors_by_volumes(db: Session, user_id: int, limit: int = 5) -> list[dict]:
    """Obtiene los autores con más tomos poseídos"""

    results = db.query(
        MangaSeries.author,
        func.count(UserMangaVolume.volume_id).label('total_volumes')
    ).join(
        MangaVolume, MangaVolume.series_id == MangaSeries.id
    ).join(
        UserMangaVolume, UserMangaVolume.volume_id == MangaVolume.id
    ).filter(
        UserMangaVolume.user_id == user_id,
        UserMangaVolume.is_owned == True,
        MangaSeries.author.isnot(None)
    ).group_by(
        MangaSeries.author
    ).order_by(
        func.count(UserMangaVolume.volume_id).desc()
    ).limit(limit).all()

    return [{"author": author, "total_volumes": int(count)} for author, count in results]


def get_top_authors_by_series(db: Session, user_id: int, limit: int = 5) -> list[dict]:
    """Obtiene los autores con más series diferentes"""

    results = db.query(
        MangaSeries.author,
        func.count(distinct(MangaSeries.id)).label('series_count')
    ).join(
        MangaVolume, MangaVolume.series_id == MangaSeries.id
    ).join(
        UserMangaVolume, UserMangaVolume.volume_id == MangaVolume.id
    ).filter(
        UserMangaVolume.user_id == user_id,
        UserMangaVolume.is_owned == True,
        MangaSeries.author.isnot(None)
    ).group_by(
        MangaSeries.author
    ).order_by(
        func.count(distinct(MangaSeries.id)).desc()
    ).limit(limit).all()

    return [{"author": author, "series_count": int(count)} for author, count in results]


def get_series_progress(db: Session, user_id: int, limit: int = 10) -> list[dict]:
    """Obtiene el progreso de colección por serie"""

    # Subconsulta: tomos poseídos por serie
    owned_subquery = db.query(
        MangaVolume.series_id,
        func.count(UserMangaVolume.volume_id).label('owned_volumes')
    ).join(
        UserMangaVolume, UserMangaVolume.volume_id == MangaVolume.id
    ).filter(
        UserMangaVolume.user_id == user_id,
        UserMangaVolume.is_owned == True
    ).group_by(
        MangaVolume.series_id
    ).subquery()

    # Query principal
    results = db.query(
        MangaSeries.id,
        MangaSeries.title,
        MangaSeries.edition_type,
        MangaSeries.total_volumes,
        func.coalesce(owned_subquery.c.owned_volumes, 0).label('owned_volumes')
    ).outerjoin(
        owned_subquery, owned_subquery.c.series_id == MangaSeries.id
    ).filter(
        owned_subquery.c.owned_volumes > 0  # Solo series con al menos 1 tomo
    ).limit(limit).all()

    series_progress = []
    for series_id, title, edition, total, owned in results:
        completion = 0.0
        if total and total > 0:
            completion = (owned / total) * 100

        series_progress.append({
            "series_id": series_id,
            "series_title": title,
            "edition_type": edition,
            "total_volumes": total,
            "owned_volumes": owned,
            "completion_percentage": round(completion, 2)
        })

    return series_progress