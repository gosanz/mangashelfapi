from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db, engine, Base
from app.models import User

app = FastAPI(title="MangaShelfAPI", description="API for storing and querying your manga collection", version="1.0")

Base.metadata.create_all(bind=engine)

#Routers
@app.get("/")
def root():
    return {"message": "Welcome to MangaShelfAPI!", "version": "1.0", "docs": "/docs"}

@app.get("/healthcheck")
def health_check():
    return {"status": "healthy"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Database connection established!", "version": "1.0", "db": db}