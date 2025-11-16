from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    options = Column(JSON, nullable=False)   # 보기 리스트
    answer = Column(String, nullable=False)   # 답
    category = Column(String, nullable=True) # 카테고리
