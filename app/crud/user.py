from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password

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
    return db.query(User).filter(User.email == email).first() # type: ignore

def get_user_by_username(db: Session, username: str) -> User | None:
    """Searches user by name"""
    return db.query(User).filter(User.username == username).first() # type: ignore