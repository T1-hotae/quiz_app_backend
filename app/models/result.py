from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_answer = Column(String)
    correct = Column(Boolean)
    solved_at = Column(DateTime(timezone=True), server_default=func.now())
