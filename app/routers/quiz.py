from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.database import get_db
from app.models.question import Question
from app.deps.auth import get_current_user

router = APIRouter()

@router.get("/random")
def random_questions(limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Question).order_by(func.random()).limit(limit).all()
