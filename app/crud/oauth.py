from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password
import secrets


def get_or_create_google_user(db: Session, google_id: str, email: str, name: str | None) -> User:
    """Obtiene o crea un usuario desde Google OAuth"""
    # Buscar por google_id
    user = db.query(User).filter(User.google_id == google_id).first()

    if user:
        return user # type: ignore

    # Buscar por email (si ya existe con otro método)
    user = db.query(User).filter(User.email == email).first()
    if user:
        # Vincular cuenta existente con Google
        user.google_id = google_id
        db.commit()
        db.refresh(user)
        return user # type: ignore

    # Crear nuevo usuario
    username = email.split('@')[0] + '_' + secrets.token_hex(4)

    new_user = User(
        email=email,
        username=username,
        google_id=google_id,
        hashed_password=None,  # OAuth no tiene password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_or_create_apple_user(db: Session, apple_id: str, email: str | None) -> User:
    """Obtiene o crea un usuario desde Apple OAuth"""
    # Buscar por apple_id
    user = db.query(User).filter(User.apple_id == apple_id).first()

    if user:
        return user # type: ignore

    # Buscar por email si existe
    if email:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.apple_id = apple_id
            db.commit()
            db.refresh(user)
            return user # type: ignore

    # Crear nuevo usuario
    email = email or f"apple_{apple_id}@mangashelf.app"
    username = f"apple_user_{secrets.token_hex(4)}"

    new_user = User(
        email=email,
        username=username,
        apple_id=apple_id,
        hashed_password=None,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user