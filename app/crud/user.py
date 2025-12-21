from sqlalchemy.orm import Session
from app.models import UserManga
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password
from datetime import datetime, timedelta, timezone
def create_user(db: Session, user: UserCreate) -> User:
    """Creates a user in the db"""
    hashed_password = hash_password(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:
    """Searches users by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> User | None:
    """Searches user by name"""
    return db.query(User).filter(User.username == username).first()

def soft_delete_user(db: Session, user_id: int) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    user.deleted_at = datetime.now(timezone.utc)
    user.is_active = False
    db.commit()
    db.refresh(user)

    return user # type: ignore

def restore_user(db: Session, username: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()

    if not user or not user.deleted_at:
        return None

    user.is_active = True
    user.deleted_at = None

    db.commit()
    db.refresh(user)

    return user # type: ignore

def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return False

    if user.deleted_at:
        grace_period = timedelta(days=15)
        if datetime.now(timezone.utc) - user.deleted_at <= grace_period:
            return False

    db.query(UserManga).filter(UserManga.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return True

def get_users_to_delete(db: Session) -> list[User]:
    grace_period_date = datetime.now(timezone.utc) - timedelta(days=15)
    return db.query(User).filter(User.deleted_at is not None, User.deleted_at <= grace_period_date).all() # type: ignore