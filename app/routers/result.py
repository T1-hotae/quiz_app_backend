from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.result import Result
from app.models.question import Question
from app.deps.auth import get_current_user

router = APIRouter()

@router.post("/submit")
def submit_answer(question_id: int, answer: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(Question).filter(Question.id == question_id).first()
    correct = q.answer == answer

    r = Result(
        user_id=user.id,
        question_id=q.id,
        user_answer=answer,
        correct=correct
    )

    db.add(r)
    db.commit()
    return {"correct": correct}
