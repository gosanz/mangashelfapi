from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db, engine, Base
from app.models import User, Manga, UserManga
from app.routers import auth
from app.dependencies.auth import get_current_active_user

app = FastAPI(title="MangaShelfAPI", description="API for storing and querying your manga collection", version="1.0")

# Create tables on DB
Base.metadata.create_all(bind=engine)

#Include Routers
app.include_router(auth.router)

#Routers
@app.get("/")
def root():
    return {"message": "Welcome to MangaShelfAPI!", "version": "1.0", "docs": "/docs"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Database connection established!", "version": "1.0", "db": db}

@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return {
        "id": current_user.id,
        "username":current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active
    }