from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.config import settings
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.schemas.oauth import GoogleAuthRequest, AppleAuthRequest
from app.crud import user as crud_user
from app.crud import oauth as crud_oauth
from app.services.oauth import verify_google_token, verify_apple_token
from app.utils.security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user"""
    db_user = crud_user.get_user_by_email(db, email=user.email) # type: ignore
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    return crud_user.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.get_user_by_username(db, username=form_data.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"},)
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"},)
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)},
                                       expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/google", response_model=Token)
async def google_auth(
        auth_data: GoogleAuthRequest,
        db: Session = Depends(get_db)
):
    """Autenticación con Google"""
    try:
        # Verificar token de Google
        user_info = await verify_google_token(auth_data.id_token)

        # Obtener o crear usuario
        user = crud_oauth.get_or_create_google_user(
            db,
            google_id=user_info["google_id"],
            email=user_info["email"],
            name=user_info.get("name")
        )

        # Generar JWT
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/apple", response_model=Token)
async def apple_auth(
        auth_data: AppleAuthRequest,
        db: Session = Depends(get_db)
):
    """Autenticación con Apple"""
    try:
        # Verificar token de Apple
        user_info = await verify_apple_token(auth_data.identity_token)

        # Obtener o crear usuario
        user = crud_oauth.get_or_create_apple_user(
            db,
            apple_id=user_info["apple_id"],
            email=auth_data.email or user_info.get("email")
        )

        # Generar JWT
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )