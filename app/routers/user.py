from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas import UserResponse, UserUpdate, PasswordChange
from app.crud.user import soft_delete_user, restore_user, update_user_password, update_user_profile, get_user_by_email, get_user_by_username

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.patch("/me", response_model=UserResponse)
def update_my_profile(user_update: UserUpdate,
                      current_user: User = Depends(get_current_active_user),
                      db: Session = Depends(get_db)):

    if user_update.email and user_update.email != current_user.email:
        if get_user_by_email(db, user_update.email): # type: ignore
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

    if get_user_by_username(db, user_update.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already in taken")

    updated_user = update_user_profile(db, current_user.id, user_update.email, user_update.username)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return updated_user

@router.post("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
def update_password(password_data: PasswordChange,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_active_user)):
    update_user = update_user_password(db, current_user.id, password_data.current_password, password_data.new_password)

    if not update_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect Password")

    return None

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def request_account_deletion(db: Session = Depends(get_db),
                             current_user: User = Depends(get_current_active_user)):
    deleted_user = soft_delete_user(db, current_user.id)

    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not delete account")

    return None


@router.post("/me/restore")
def restore_my_account(db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_active_user)):
    restored_user = restore_user(db, current_user.id)

    if not restored_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not restore account (grace period expired or account not deleted)")

    return restored_user